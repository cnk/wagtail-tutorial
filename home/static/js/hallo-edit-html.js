(function() {
  (function($) {
    return $.widget('IKS.edithtml', {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;
        // noinspection JSUnusedLocalSymbols
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
          label: 'Edit HTML',
          icon: 'icon icon-code',
          command: null
        });

        toolbar.append(button);

        button.on('click', function() {
          $('body > .modal').remove();
          var container = $(
           `<div class="modal fade edit-html-dialog" tabindex="-1" role="dialog" aria-hidden="true">
              <div class="modal-dialog">
                <div class="modal-content">
                  <button type="button" class="button close button--icon text-replace" data-dismiss="modal">
                    <svg class="icon icon-cross" aria-hidden="true"><use href="#icon-cross"></use></svg>Close
                  </button>
                  <div class="modal-body">
                    <header class="w-header w-header--merged">
                      <div class="row">
                        <div class="left">
                          <div class="col">
                            <h1 class="w-header__title" id="header-title">
                              <i class="w-header__glyph icon icon-fa-file-code-o" style="font-size: small;"></i>Edit HTML Code
                            </h1>
                          </div>
                        </div>
                    </header>
                    <div class="modal-form"></div>
                  </div>
                </div>
              </div>
            </div>`
          );

          // Add container to body and hide it, so content can be added to it before display.
          $('body').append(container);
          container.modal('hide');
          // Stick the HTML to be edited into a textarea. Note that this will escape the HTML under edit,
          // which is what we want. Otherwise, if the HTML under edit had a textarea in it, the UI would get confused.
          var editor = $('<textarea id="wagtail-edit-html-content"></textarea>');
          editor.text(widget.options.editable.element.html());
          var save_button = '<button id="wagtail-edit-html-save" type="button">Save</button>';
          // Stick the editor and save button into the modal body, then show the container.
          container.find('.modal-form').append(editor).append(save_button);
          container.modal('show');

          $('#wagtail-edit-html-save').on('click', function() {
            var edited_html = $('#wagtail-edit-html-content').val();
            widget.options.editable.setContents(edited_html);
            widget.options.editable.setModified();
            container.modal('hide');
          });
        });
      }
    });
  })(jQuery);
}).call(this);
