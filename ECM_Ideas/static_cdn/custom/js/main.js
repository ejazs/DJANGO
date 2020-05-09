function like_toggle_js(e){
  e.preventDefault();
  var this_ = $(this);
  var url_ = this_.attr('data-href');
  $.ajax(
   {
    url : url_,
    type : 'GET',
    data : {},
    success : function(data){
      if(data["liked"]){
        // $(this_).find('i').toggleClass('fa-thumbs-up fa-thumbs-down');
        $(this_).find('i').text("Liked");   
        
        (this_).css('color','#2196f3')
        $(this_).find('span').text(data.total_likes);          
      }
      else
      {
       
        // $(this_).find('i').toggleClass('fa-thumbs-up fa-thumbs-down');
        $(this_).find('i').text("Like");
        $(this_).css('color','#18BC9C')
        $(this_).find('span').text(data.total_likes);    
        
      }   
    }
   }
  )
}