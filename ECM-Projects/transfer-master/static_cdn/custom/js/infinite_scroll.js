function myInfiniteScroll(){
  var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
      $('.loading').show();
    },
    onAfterPageLoad: function ($items) {
      $('.loading').hide();
    }
  });
  
  
  
  $( document ).ajaxComplete(function() {
  // console.log( "Triggered ajaxComplete handler." );
  all_imgs = $('.card-body img');
  all_imgs.each(function(){$(this).addClass('img-fluid')})
  });
}
