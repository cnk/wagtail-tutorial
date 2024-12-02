'use strict';

(function() {
  (function($) {
    return $.widget('IKS.subscript', {
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
          label: 'Subscript',
          icon: 'icon-subscript',
          command: null,
          queryState: function(event) {
            return button.hallobutton('checked', !!getEnclosing("sub"));
          }
        });

        toolbar.append(button);

        button.on('click', function(event) {
          return widget.options.editable.execute(
            getEnclosing("sub") ? 'removeFormat': 'subscript');
        });

      }
    });
  })(jQuery);
}).call(this);
