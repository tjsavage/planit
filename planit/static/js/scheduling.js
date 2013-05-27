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

        this.blocksByDay = {}
        for (var i = 0; i < Scheduler.days.length; i++) {
            this.blocksByDay[Scheduler.days[i]] = [];
        }

        this.on("change", this.change, this);
        this.on("add", this.added, this);
        this.on("reset", this.wasReset, this);
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

    wasReset: function() {
        for(var i = 0; i < this.length; i++) {
            var block = this.at(i);
            this.blocksByDay[block.get("day")].push(block);
        }
        this.trigger("ready");
    },

    change: function() {
        this.update();
    },

    added: function(model) {
        console.log(model);
    }
});

Scheduler.ScheduleBlockView =  Backbone.View.extend({
    initialize: function() {
        this.on("slide:complete", this.slideComplete, this);
        this.on("makeSlider", this.makeSlider, this);
    },

    render: function() {
        var template;

        if (parseInt(this.model.get("start").substring(0, 2)) % 2) {
            template = _.template( $("#block-template-odd").html());
        } else {
            template = _.template( $("#block-template-even").html());
        }
        if (this.model.get("start").indexOf("30") == -1) {
            this.$el.css("float", "left");
        } else {
            this.$el.css("float", "right");
        }

        this.$el.html(template(this.model.toJSON()));
        this.$el.addClass("iosSlider1");

        return this;
    },

    slideComplete: function(args) {
        if (args.currentSlideNumber == 1) { //free
            this.model.set("busy", false);
        } else {
            this.model.set("busy", true);
        }
    },

    makeSlider: function() {
        var T = this;
        this.$el.iosSlider({
            snapToChildren: true,
            desktopClickDrag: true,
            infiniteSlider: true,
            startAtSlide: this.model.get("busy") ? 2 : 1,
            onSlideComplete: function(args) {
                T.trigger("slide:complete", args);
            }
        });
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
            var $sliderContainer = this.$el.find(".block-slider-container");
            $sliderContainer.html("");
            for(var i = 0; i < this.model.blocksByDay[this.day].length; i++) {
                block = this.model.blocksByDay[this.day][i];
                view = new Scheduler.ScheduleBlockView({model: block});
                this.renderBlockView(view, $sliderContainer);
            }
         
            this.trigger("drew");   
            this.drawn = true;
        }
    },

    renderBlockView: function(view, $sliderContainer) {
        setTimeout(function() {
            view.render();
            $sliderContainer.append(view.el);
            view.trigger("makeSlider");
        }, 100);
            
    }
});

$(function() {
    var schedule = new Scheduler.Schedule([], {user_id: $("#user-id").html() });

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
            dayView = Scheduler.dayViews[Scheduler.days[dayIndex]]
            if (!dayView.drawn) {
                dayView.trigger("draw");
            }
        }
    });

    schedule.fetch({
        reset: true,
        update: true
    });

    schedule.on("ready", function() {
        Scheduler.dayViews["Sunday"].trigger("draw")
    });

});