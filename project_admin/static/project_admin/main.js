$(document).ready(function(){
    $("#groupModal").on('show.bs.modal', function (e) {
      var member_id = $(e.relatedTarget).data('member_id');
      console.log(member_id);
      $('#groupModalBody').load('/group_modal_body/'+member_id);
      $('#member_title').html(member_id);
      $('#addGroupLink').attr('data-member_id',member_id);
    });
    $("#addGroupModal").on('show.bs.modal', function (e) {
      var member_id = $(e.relatedTarget).data('member_id');
      console.log(member_id);
      $('#addGroupModalBody').load('/group_modal_add_body/'+member_id);
      $('#groups_member_title').html(member_id);
      //$('#detailId').attr("href", '/notebook/'+member_id);
      //document.getElementById("notebook_filler").innerHTML = "new content"
        ///alert('The modal will show'+nbid);
    });
    $("#notesModal").on('show.bs.modal', function (e) {
      var member_id = $(e.relatedTarget).data('member_id');
      console.log(member_id);
      $('#notesModalBody').load('/notes_modal_body/'+member_id);
      $('#notes_member_title').html(member_id);
      $('#addNoteLink').attr('data-member_id',member_id);
    });
    $("#addNoteModal").on('show.bs.modal', function (e) {
      var member_id = $(e.relatedTarget).data('member_id');
      console.log(member_id);
      $('#addNoteModalBody').load('/notes_modal_add_body/'+member_id);
      $('#new_notes_member_title').html(member_id);
    });
    $("#filesModal").on('show.bs.modal', function (e) {
      var member_id = $(e.relatedTarget).data('member_id');
      console.log(member_id);
      $('#filesModalBody').load('/files_modal_body/'+member_id);
      $('#files_member_title').html(member_id);
    });
    $('[data-toggle="tooltip"]').tooltip();
});
