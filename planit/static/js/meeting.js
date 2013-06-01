var Meeting = function() {
};

Meeting.Meeting = Backbone.Model.extend({
    initialize: function() {
        this.fetch();

        this.suggestedTimeList = new Meeting.SuggestedTimeList([], {meeting_id: this.get("id")});
        this.on("save", this.save, this);
    },

    fetch: function() {
        var T = this;
        $.ajax({
            type: "GET",
            url: this.url(),
            dataType: "json",
            success: function(data) {
                T.set(data);
            }
        });
    },

    save: function() {
        this.suggestedTimeList.saveAll();
    },

    url: function() {
        return "/api/meeting/" + this.get("id") + "/";
    }

});

Meeting.SuggestedTime = Backbone.Model.extend({
    initialize: function() {
        this.on("set:declined", this.declined, this);
        this.on("set:accepted", this.accepted, this)
    },

    update: function() {
        if(this.get("status") == "declined") {
            $.ajax({
                url: this.url(),
                type: "DELETE"
            });
        } else {
            $.ajax({
                url: this.url(),
                type: "POST"
            });
        }
    },

    declined: function() {
        this.set("status", "declined");
        this.update();
    },

    accepted: function() {
        this.set("status", "accepted");
        this.update();
    },

    url: function() {
        return "/api/meeting/" + this.get("meeting_id") + "/availability/" + this.get("pk") + "/";
    }


});

Meeting.SuggestedTimeList = Backbone.Collection.extend({
    model: Meeting.SuggestedTime,

    initialize: function(models, options) {
        this.meeting_id = options.meeting_id;

        this.on("add", this.added, this);
        this.on("reset", this.wasReset, this);

        this.fetch();
    },

    saveAll: function() {
        this.each(function(model) {
            model.update();
        });
    },

    url: function() {
        return "/api/meeting/" + this.meeting_id + "/availability/";
    },

    added: function(model) {
        model.set({meeting_id: this.meeting_id});
        model.fetch();
    }
});

Meeting.SuggestedTimeView =  Backbone.View.extend({
    initialize: function() {
        this.on("slide:complete", this.slideComplete, this);
        this.on("makeSlider", this.makeSlider, this);
        this.model.on("change", this.changed, this);
    },

    render: function(type) {
        var template;
        if (type == "even") {
            template = _.template( $("#block-template-even").html());
        } else {
            template = _.template( $("#block-template-odd").html());
        }

        this.$el.html(template(this.model.toJSON()));
        this.$el.addClass("iosSlider1 iosSlider1-full");

        return this;
    },

    changed: function() {
        if (this.model.get("status") == "declined") {
            this.$el.iosSlider('goToSlide', 2);
        } else {
            this.$el.iosSlider('goToSlide', 1);
        }
    },

    slideComplete: function(args) {
        if (args.currentSlideNumber == 1) { //free
            this.model.trigger("set:accepted");
        } else {
            this.model.trigger("set:declined");
        }
    },

    makeSlider: function() {
        var T = this;
        this.$el.iosSlider({
            snapToChildren: true,
            desktopClickDrag: true,
            infiniteSlider: true,
            startAtSlide: this.model.get("status") == "declined" ? 2 : 1,
            onSlideComplete: function(args) {
                T.trigger("slide:complete", args);
            }
        });
    }
});

Meeting.SuggestedTimeListView = Backbone.View.extend({
    initialize: function() {
        this.model.on("add", this.added, this);
    },

    added: function(suggestedTime) {
        var view = new Meeting.SuggestedTimeView({model: suggestedTime});
        var type = this.model.indexOf(suggestedTime) % 2 ? "even" : "odd";
        this.$el.append(view.render(type).el);
        view.trigger("makeSlider");
    }
});


$(function() {
    setupAjaxCsrf();
    var meeting = new Meeting.Meeting({id: $("#meeting-id").html() });
    var timeList = new Meeting.SuggestedTimeListView({model: meeting.suggestedTimeList, el: $("#suggested-time-list")});
    $("#save-button").click(function() {
        meeting.trigger("save");
        return false;
    });
});