(function() {
  (function($) {
    return $.widget('IKS.superscript', {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;
        var getEnclosing = function(tag) {
          var node;
          node = widget.options.editable.getSelection().commonAncestorContainer;
          return $(node).parents(tag).get(0);
        };

        widget = this;

        button = $('<span></span>');
        button.hallobutton({
          uuid: this.options.uuid,
          editable: this.options.editable,
          label: 'Superscript',
          icon: 'icon-superscript',
          command: null,
          queryState: function(event) {
            return button.hallobutton('checked', !!getEnclosing("sup"));
          }
        });

        toolbar.append(button);

        button.on('click', function(event) {
          return widget.options.editable.execute(
            getEnclosing("sup") ? 'removeFormat': 'superscript');
        });

      }
    });
  })(jQuery);
}).call(this);
