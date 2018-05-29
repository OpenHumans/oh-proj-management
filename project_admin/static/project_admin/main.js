$(document).ready(function() {
     $('#myModal').on('show.bs.modal', function(e) {
        var member = $(e.relatedTarget).data('member')
        var groups = $(e.relatedTarget).data('groups')
        var membergroups = $(e.relatedTarget).data('membergroups')
        var modal = $(this)
        modal.find('.form-group select option').val(groups) 
    })
 });
