$(document).ready(function(){
    $('.btn-refresh').on('click', function(e){
        var self = this;
        e.preventDefault();

        var accountId = $(self).data('account');
        $('.fa', self).addClass('fa-spin');

        $.ajax({
            url: '/api/accounts/'+accountId+'/refresh'
        }).success(function(){
            window.location.reload();
        }).fail(function(){
            $('.fa', self).removeClass('fa-spin');
        });
    });

    $('.action-accept').on('click', function(e){
        e.preventDefault();

        var index = $(this).data('index');
        var accountId = $(this).data('account');

        $('#inbox-'+index).css('opacity', 0.5);
        $('#inbox-'+index+' button').prop('disabled', true);

        $.ajax({
            url: '/api/accounts/'+accountId+'/inbox/accept',
            contentType: 'application/json',
            data: JSON.stringify({indices: [index]}),
            method: 'PUT'
        }).success(function(data){
            window.location.reload();
        }).fail(function(data){
            $('#inbox-'+index).css('opacity', 1);
            $('#inbox-'+index+' button').prop('disabled', false);
        });
    });

    $('#send-form').on('submit', function(e){
        e.preventDefault();
        var data = $(":input", this).serializeArray();
        var obj = {};
        for (var i = data.length - 1; i >= 0; i--) {
            obj[data[i].name] = data[i].value;
        }

        $.ajax({
            url: '/api/transaction/transfer',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(obj)
        }).success(function(data){
            $('#send-form .result').addClass('alert alert-success')
            .text('Success!');
            $('#send-form :input').val('');
        }).fail(function(data){
            $('#send-form .result').addClass('alert alert-danger')
            if (data.responseText && data.responseJSON && data.responseJSON.error) {
                $('#send-form .result').text(JSON.stringify(data.responseJSON.error));
            } else {
                $('#send-form .result').text('Unexpected error ocurred.');
            }
        })
    });

    if (window.desktop) {
        $('.copy-clipboard').on('click', function(){
            var text = $(this).data('clipboard');
            alert(JSON.stringify({"instruction": "clipboard", "value": text}));
        });
    } else {
        $('.copy-clipboard').zclip({
            path:'/static/libs/ZeroClipboard.swf',
            copy: function() {
                return $(this).data('clipboard');
            },
            afterCopy: function() {}
        });
    }

    /* setup/step1.html */
    $('#add-server').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: '/api/wallet/server',
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                contract: $('#server-contract').val()
            })
        }).done(function(data){
            window.location.replace("/");
        });
    });
    /* end - setup/step1.html */

    /* setup/step2.html */
    $('#new-nym').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: '/api/nyms',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                name: $('#nym-name').val()
            })
        }).done(function(){
            window.location.replace("/");
        });
    });
    /* end - setup/step2.html */

    /* setup/step3.html */
    $('#existing-asset-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: '/api/wallet/asset',
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                contract: $('#existing-asset-contract').val()
            })
        }).done(function(data){
            window.location.replace("/");
        });
    });
    /* end - setup/step3.html */

    /* setup/step4.html */
    $('#change-account-name').on('submit', function(e){
        e.preventDefault();
        var myAccId = $('#account-id').val();
        var name = $('#account-name').val();
        url = encodeURI('/api/accounts/'+myAccId+'/name/'+name)
        $.ajax({
            url: url,
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json'
        }).done(function(){
            window.location.replace("/");
        });
    });
    /* end - setup/step4.html */

    var setupAssetOption = null;
    $('.new-asset .btn-existing-asset').on('click', function(e){
        e.preventDefault();
        if (setupAssetOption && setupAssetOption != 'existing') {
            $('.issue-asset-container').slideUp('fast', function(){
                setupAssetOption = 'existing';
                $('.existing-asset-container').slideDown();
            });
        } else {
            setupAssetOption = 'existing';
            $('.existing-asset-container').slideDown();
        }
    });

    $('.new-asset .btn-issue-asset').on('click', function(e){
        e.preventDefault();
        if (setupAssetOption && setupAssetOption != 'new') {
            $('.existing-asset-container').slideUp('fast', function(){
                setupAssetOption = 'new';
                $('.issue-asset-container').slideDown();
            });
        } else {
            setupAssetOption = 'new';
            $('.issue-asset-container').slideDown();
        }
    });

    $('#issue-asset-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: '/api/assets/issue',
            method: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                contract: $('#issue-asset-contract').val(),
                serverId: $('#issue-asset-server').val(),
                myNymId: $('#issue-asset-nym').val()
            })
        }).success(function(data){
            window.location.replace("/");
        }).fail(function(data){
            $('#issue-asset-form .result').addClass('alert alert-danger');
            $('#issue-asset-form .result').text(JSON.stringify(data.responseJSON.error));
        });
    });
});