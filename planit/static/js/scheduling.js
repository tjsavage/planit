var Scheduler = {
    days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
};

Scheduler.ScheduleBlock = Backbone.Model.extend({
    initialize: function() {}
});

Scheduler.Schedule = Backbone.Collection.extend({
    initialize: function(models, options) {
        this.user_id = options.user_id;

        this.on("change", this.change, this);
    },

    url: function() {
        return "/api/schedule/" + this.user_id + "/";
    },

    change: function() {
        console.log("changed");
        this.sync();
    }
});

Scheduler.ScheduleBlockView =  Backbone.View.extend({
    initialize: function() {
        this.on("slide:complete", this.slideComplete, this);
    },

    render: function() {
        var template = _.template( $("#block-template").html())
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
        this.model.on("add", this.add, this);
    },

    render: function() {
        var template = _.template( $("#day-template").html());
        this.$el.html(template({"day": this.day}));
        this.$el.addClass("day-slide");
        return this;
    },

    add: function(model) {
        if (model.get("day") == this.day) {
            var view = new Scheduler.ScheduleBlockView({model: model});
            this.$el.find(".block-slider-container").append(view.render().el);
            this.$el.find('.iosSlider1').iosSlider({
                snapToChildren: true,
                desktopClickDrag: true,
                infiniteSlider: true,
                onSlideComplete: function(args) {
                    view.trigger("slide:complete", args);
                }
            });
        }
    }
})

$(function() {
    var schedule = new Scheduler.Schedule([], {user_id: 1});

    for (var i = 0; i < Scheduler.days.length; i++) {
        var scheduleDayView = new Scheduler.ScheduleDayView({model: schedule,
                                                        day: Scheduler.days[i]});
        $("#day-slider").append(scheduleDayView.render().el);
    }

    $("#day-slider-container").iosSlider({
        snapToChildren: true,
        desktopClickDrag: true,
        navPrevSelector: $(".slider-button.slider-prev-button"),
        navNextSelector: $(".slider-button.slider-next-button"),
        unselectableSelector: $(".block-slider-container")
    });

    schedule.fetch();

});