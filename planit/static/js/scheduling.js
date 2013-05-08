var Scheduler = {
    days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    dayViews: {}
};

Scheduler.ScheduleBlock = Backbone.Model.extend({
    initialize: function() {}
});

Scheduler.Schedule = Backbone.Collection.extend({
    initialize: function(models, options) {
        this.user_id = options.user_id;

        this.on("change", this.change, this);
        this.on("add", this.added, this);
    },

    url: function() {
        return "/api/schedule/" + this.user_id + "/";
    },

    update: function() {
        $.ajax({
            type: "POST",
            url: this.url(),
            data: JSON.stringify(this.toJSON()),
            dataType: "json"
        });
    },

    change: function() {
        this.update();
    },

    added: function(model) {
        console.log("added");
    }
});

Scheduler.ScheduleBlockView =  Backbone.View.extend({
    initialize: function() {
        this.on("slide:complete", this.slideComplete, this);
    },

    render: function() {
        var template = _.template( $("#block-template").html());
        this.$el.html(template(this.model.toJSON()));
        this.$el.addClass("iosSlider1");

        if (this.model.get("start").indexOf("30") == -1) {
            this.$el.css("float", "left");
        } else {
            this.$el.css("float", "right");
        }
        if (parseInt(this.model.get("start").substring(0, 2)) % 2) {
            this.$el.find(".block-slide-free").addClass("odd free");
            this.$el.find(".block-slide-busy").addClass("odd busy");
        } else {
            this.$el.find(".block-slide-free").addClass("even free");
            this.$el.find(".block-slide-busy").addClass("even busy");
        }
        return this;
    },

    slideComplete: function(args) {
        if (args.currentSlideNumber == 1) { //free
            this.model.set("busy", false);
        } else {
            this.model.set("busy", true);
        }
    }
});

Scheduler.ScheduleDayView = Backbone.View.extend({
    initialize: function(options) {
        this.day = options.day;
        this.on("add:block", this.addBlock, this);
        this.drawn = false;
        this.on("draw", this.drawBlocks, this);
    },

    render: function() {
        var template = _.template( $("#day-template").html());
        this.$el.html(template({"day": this.day}));
        this.$el.addClass("day-slide");
        return this;
    },

    drawBlocks: function() {
        if (!this.drawn) {
            var T = this;

            $.each(this.model.filter(function(block) {
                return block.get("day") == T.day;
            }), function(i, block) {
                T.trigger("add:block", block);
            });
            this.trigger("drew");   
            this.drawn = true;
        }
    },

    addBlock: function(model) {
        if (model.get("day") == this.day) {
            var view = new Scheduler.ScheduleBlockView({model: model});
            this.$el.find(".block-slider-container").append(view.render().el);
            this.$el.find('.iosSlider1').iosSlider({
                snapToChildren: true,
                desktopClickDrag: true,
                infiniteSlider: true,
                startAtSlide: model.get("busy") ? 2 : 1,
                onSlideComplete: function(args) {
                    view.trigger("slide:complete", args);
                }
            });
        }
    }
});

$(function() {
    var schedule = new Scheduler.Schedule([], {user_id: 1});

    for (var i = 0; i < Scheduler.days.length; i++) {
        var day = Scheduler.days[i];
        var scheduleDayView = new Scheduler.ScheduleDayView({model: schedule,
                                                        day: day});
        $("#day-slider").append(scheduleDayView.render().el);
        Scheduler.dayViews[day] = scheduleDayView;
    }

    $("#day-slider-container").iosSlider({
        snapToChildren: true,
        desktopClickDrag: true,
        navPrevSelector: $(".slider-button.slider-prev-button"),
        navNextSelector: $(".slider-button.slider-next-button"),
        unselectableSelector: $(".block-slider-container"),
        onSlideComplete: function(args) {
            var dayIndex = args.currentSlideNumber - 1;
            if (dayIndex < 5) {
                var nextDay = Scheduler.days[dayIndex + 2];
                Scheduler.dayViews[nextDay].trigger("draw");
            }
        }
    });

    schedule.fetch({
        success: function() {
            Scheduler.dayViews["Sunday"].trigger("draw");
            Scheduler.dayViews["Monday"].trigger("draw");
            Scheduler.dayViews["Tuesday"].trigger("draw");
        }
    });

});