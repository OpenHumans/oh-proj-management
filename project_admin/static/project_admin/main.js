$(document).ready(function(){
    $("#groupModal").on('show.bs.modal', function (e) {
      var member_id = $(e.relatedTarget).data('member_id');
      console.log(member_id)
      $('#groupModalBody').load('/group_modal_body/'+member_id);
      $('#member_title').html(member_id);
      //$('#detailId').attr("href", '/notebook/'+member_id);
      //document.getElementById("notebook_filler").innerHTML = "new content"
        ///alert('The modal will show'+nbid);
    });
    $('[data-toggle="tooltip"]').tooltip();
});
