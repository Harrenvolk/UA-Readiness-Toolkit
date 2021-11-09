$(document).ready(function () {

    $.getJSON("/config", function(res) {
        for(const [key, _] of Object.entries(res.languages)){
            $("#sel-lang").append($('<option>', {
                value: key,
                text: key
            }));
        }
    }).fail(function () {
        alert("ER!");
    })

    $('.testcase .edit').click(function () {
        var idx = $(this).attr('id').split('-')[1];
        var href = $(this).prop('href');
        if (!href) {
            $('#inp-' + idx).prop('disabled', false);
            $(this).prop('href', '/update_test_url/' + idx);
            $(this).removeClass('btn-outline-info');
            $(this).addClass('btn-outline-success');
            $(this).text("Submit");
        } else {
            $.ajax({
                url: href,
                type: "POST",
                data: {
                    new_url: $('#inp-' + idx).val()
                },
                success: function (msg) {
                    location.reload();
                },
                fail: function (xhr, textStatus, errorThrown) {
                    alert("There was an unexpected error! Please try again.");
                }
            })
        }
        return false;
    })

    $('.testcase .delete').click(function () {
        var href = $(this).prop('href');
        $.ajax({
            url: href,
            type: "POST",
            success: function (msg) {
                location.reload();
            },
            fail: function (xhr, textStatus, errorThrown) {
                alert("There was an unexpected error! Please try again.");
            }
        })
        return false;
    })

});