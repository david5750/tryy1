$(document).ready(function () {

    $('.blogo').click(function () {
        $('.logosubmenu').toggle();
    });
    $('li').click(function () {
        $('.logosubmenu').toggle();
    });

    $('#deletefolder').click(function () {
        $('.foldericon').removeClass('fa-bars');
        $('.foldericon').addClass('fa-trash-o');
    });

    $('.fa-trash-o').click(function () {
        console.log("trash clicked ");
        let datasid = $(this).attr('data-sid');
        console.log(datasid);
    });

    //DEL FOLDER
    $('div').on('click', '.fa-trash-o', function () {
        console.log("trash clicked ");
        let user_random = $("random1").val();
        let datasid = $(this).attr('data-sid');
        console.log(datasid);
        $('.foldericon').removeClass('fa-trash-o');
        $('.foldericon').addClass('fa-bars');
        alert('confrm it');
        let csr = $("input[name=csrfmiddlewaretoken]").val();
        console.log(this);
        $(this).parent().fadeOut();


        $.ajax({
            url: 'delfolder',
            method: "POST",
            data: { data_sid: datasid, csrfmiddlewaretoken: csr, user_random: user_random },
            success: function (data) {
                $('#random2').val('');
                console.log(data.status);
            }
        });

    });


});

//No folder selected
$(document).ready(function () {
    $('body').on('click', function () {
        console.log('2 nspart');
        let random2 = $('#random2').val();
        console.log(random2);
        if (random2 == "") {
            console.log('suces no folder selected');
            $('.part2-2b').hide();
            $('body').append("<div class='w3-display-middle nofolder' > <i class='fa fa-sticky-note-o fa-5x' aria-hidden='true'></i> <br> <h2>NO folder selected</h2></div>");
        }
        else {
            $('.part2-2b').show();
            $('.nofolder').hide();

        }
    })


})









