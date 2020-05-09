// // Call the dataTables jQuery plugin
// $(document).ready(function() {
//   $('#dataTable').DataTable({
//     // dom: 'Bfrtip',
//     buttons : ["copy"]
//   });
// });


$(document).ready(function() {
  $('#dataTable').DataTable( {
      dom: 'Bfrtip',
      buttons: [
          'copyHtml5',
          'excelHtml5',
          'csvHtml5',
          'pdfHtml5'
      ]
  } );
  $(":button").addClass("btn btn-primary");
   // Add event listeners to the two range filtering inputs
  //  $('#min').keyup( function() { table.draw(); } );
  //  $('#max').keyup( function() { table.draw(); } );
} );