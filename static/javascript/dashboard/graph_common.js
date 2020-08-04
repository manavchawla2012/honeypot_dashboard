function convert_multiselect(selector) {
    selector.find(".multi-tag").select2({
        tags: true,
        tokenSeparators: [',', ' '],
    })
}

function sendFormData(url, visualize_graph_btn, save_graph_btn, save_data) {
    $('.element-error').remove()
    let graph_view = $(".graph_view")
    let form_data = {}
    var csrftoken = $("[name='csrfmiddlewaretoken']").val();
    visualize_graph_btn.addClass("disabled")
    $("#graph-form").find('input, select, textarea').each(function (index, node) {
        let input = $(this);
        let input_name = input.attr("name")
        if (input_name) {
            form_data[input_name] = input.val()
        }
    });
    $.ajax({
        url: url,
        method: "post",
        dataType: "json",
        cache: true,
        async: true,
        headers: {"X-CSRFToken": csrftoken},
        data: {data: JSON.stringify(form_data), save: save_data},
        success: function (data) {
            graph_view.html("");
            if (data.success) {
                graph_view.html("")
                graph_view.append("<div id='chart-test' style='width: 100%; height: 100%'></div>")
                let graph_type = $("[name=graph_type]").val()
                create_chart(parseInt(graph_type), data["msg"], "chart-test", 0)
                if (save_data) {
                    visualize_graph_btn.addClass("hide")
                    save_graph_btn.addClass("disabled")
                } else {
                    save_graph_btn.removeClass("hide")
                }
            } else {
                let error_msg = data["msg"]
                printErrors(error_msg)
                graph_view.html(error_msg)
            }
            visualize_graph_btn.removeClass("disabled")
        },
        error: function () {
            alert("Please Refresh Page")
        }
    })
}

function printErrors(error_list) {
    if(error_list) {
        error_list.forEach(function (val, i) {
            for (let msg_name in val) {
                $("<div class='alert alert-danger element-error'>" + val[msg_name] + "</div>").insertBefore(`[name=${msg_name}]`)
            }
        })
    }
}

function handleCheckedInput() {
    let checkboxes = $("#graph-form").find("input[type=checkbox]")
    checkboxes.val(function () {
        return $(this).is(":checked");
    })
    checkboxes.on("click", function () {
        let is_checked = $(this).is(":checked")
        $(this).val(is_checked)
    })
}

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(selector, prefix) {
    $(".multi-tag").select2("destroy")
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function () {
        if ($(this).attr('name')) {
            var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });
    newElement.find('label').each(function () {
        var forValue = $(this).attr('for');
        if (forValue) {
            forValue = forValue.replace('-' + (total - 1) + '-', '-' + total + '-');
            $(this).attr({'for': forValue});
        }
    });
    newElement.find('div').each(function () {
        var id = $(this).attr("id")
        if (id) {
            id = id.replace('-' + (total - 1) + '-', '-' + total + '-')
            $(this).attr({id: id})
        }
    })
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
        .removeClass('btn-success').addClass('btn-danger')
        .removeClass('add-form-row').addClass('remove-form-row')
        .html('<span class="glyphicon glyphicon-minus" aria-hidden="true"></span>');
    convert_multiselect($(".multi-tag"))
    return false;
}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1) {
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).find(':input').each(function () {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}

function add_delete_formset_buttons() {
    $(document).on('click', '.add-form-row', function (e) {
        e.preventDefault();
        cloneMore('.form-row:last', 'form');
        convert_multiselect($(".form-row"));
        handleCheckedInput();
        return false;
    });
    $(document).on('click', '.remove-form-row', function (e) {
        e.preventDefault();
        deleteForm('form', $(this));
        return false;
    });
}
