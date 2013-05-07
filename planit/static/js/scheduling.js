var Scheduler = {
    days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
};

Scheduler.ScheduleBlock = Backbone.Model.extend({
    initialize: function() {}
});

Scheduler.Schedule = Backbone.Collection.extend({
    initialize: function(models, options) {
        this.user_id = options.user_id;
    },

    url: function() {
        return "/api/schedule/" + this.user_id + "/";
    }
});

Scheduler.ScheduleBlockView =  Backbone.View.extend({
    render: function() {
        var template = _.template( $("#schedule-block-template").html())
        this.$el.html(template(this.model.toJSON()));
        this.$el.addClass("iosSlider1");
        console.log(this.model.get("start").indexOf("30"));
        if (this.model.get("start").indexOf("30") == -1) {
            this.$el.css("float", "left");
        } else {
            this.$el.css("float", "right");
        }
        if (parseInt(this.model.get("start").substring(0, 2)) % 2) {
            this.$el.find(".item1").addClass("odd-green");
            this.$el.find(".item2").addClass("odd-red");
        } else {
            this.$el.find(".item1").addClass("even-green");
            this.$el.find(".item2").addClass("even-red");
        }
        return this;
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

        return this;
    },

    add: function(model) {
        if (model.get("day") == this.day) {
            var view = new Scheduler.ScheduleBlockView({model: model});
            this.$el.find(".schedule-block-container").append(view.render().el);
            this.$el.find('.iosSlider1').iosSlider({
                snapToChildren: true,
                desktopClickDrag: true
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
    /*
    $(document).on("pageinit", "#schedule-page", function() {
        $(document).on("swiperight swipeleft", "#schedule-page", function(e) {
            if ($.mobile.activePage.jqmData("panel") !== "open") {
                if (e.type === "swipeRight") {
                    $("#left-panel").panel("open");
                } else if (e.type === "swipeLeft") {
                    $("#left-panel").panel("close");
                }
            }
        });
    });
*/
    schedule.fetch();

});