$(function() {
    $('.input-with-button').on('click', 'a', function() {
        var $this = $(this);
        var length = $this.data('length');
        var chars = $this.data('chars');
        var result = "";

        while(length--) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }

        $this.closest('.input-with-button').find('input').val(result);
    });
});
