$(document).ready(function() {
    $( "select" ).change(function(event) {
        window.location = $( this ).val();
    });
});
