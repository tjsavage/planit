var PersonList = function(options) {
};

PersonList.PersonModel = Backbone.Model.extend({
    initialize: function() {
    }
});

PersonList.PersonList = Backbone.Collection.extend({
    model: PersonList.PersonModel
});

PersonList.PersonView = Backbone.View.extend({
    template: '<span class="fui-cross-16" id="person-remove"></span>&nbsp;&nbsp; <%= name %>: <%= phone %>',

    render: function() {
        var template = _.template(this.template, this.model.toJSON());

        this.$el.html(template);
        var T = this;
        this.$el.find("#person-remove").click(function() {
            T.remove();
            T.model.destroy();
        });
        return this;
    }
});

PersonList.PersonListView = Backbone.View.extend({
    initialize: function() {
        if(!this.model) {
            this.model = new PersonList.PersonList();
        }
        this.model.on("add", this.addedPerson, this);
        this.render();
    },

    render: function() {
        var html = '<div><input type="text" value placeholder="Name" id="person-name"> <input type="text" value placeholder="Number" id="person-phone"> &nbsp; <a href="#" id="plus-button" class="btn btn-primary btn-small">+</a></div><div id="person-list"></div>';
        this.$el.html(html);
        this.personNameField = this.$el.find("#person-name");
        this.personPhoneField = this.$el.find("#person-phone");
        this.personList = this.$el.find("#person-list");
        var T = this;
        this.$el.find("#plus-button").click(function() {
            T.clickedAdd();
            return false;
        });
    },

    addedPerson: function(person) {
        var personView = new PersonList.PersonView({model: person});
        this.personList.append(personView.render().el);
    },

    clickedAdd: function() {
        var newPerson = new PersonList.PersonModel({
            name: this.personNameField.val(),
            phone: this.personPhoneField.val()
        });
        this.model.add(newPerson);

        this.personNameField.val("");
        this.personPhoneField.val("");
    }
});