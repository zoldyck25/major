// for animation testimonial slider 


$(document).ready(function(){

    
    // hide-left       

     $('.item-1').on('click', function(event){ 
         $(".look").addClass('hide-left');
         $(".hide-left").removeClass('look');
         $('.item-text-1').addClass('look');
         $('.item-text-1').removeClass('hide-left', 'hide-right');


         $(".nav-img").removeClass('active');
         $(this).addClass('active');
     });

     $('.item-2').on('click', function(event){ 
         $(".look").addClass('hide-left');
         $(".hide-left").removeClass('look');
         $('.item-text-2').addClass('look');
         $('.item-text-2').removeClass('hide-left', 'hide-right');  


         $(".nav-img").removeClass('active');
         $(this).addClass('active');   
     });

     $('.item-3').on('click', function(event){ 
         $(".look").addClass('hide-left');
         $(".hide-left").removeClass('look');
         $('.item-text-3').addClass('look');
         $('.item-text-3').removeClass('hide-left', 'hide-right');   


         $(".nav-img").removeClass('active');
         $(this).addClass('active');  
     });

     $('.item-4').on('click', function(event){ 
         $(".look").addClass('hide-left');
         $(".hide-left").removeClass('look');
         $('.item-text-4').addClass('look');
         $('.item-text-4').removeClass('hide-left', 'hide-right');  


         $(".nav-img").removeClass('active');
         $(this).addClass('active');   
     });
     
     $('.item-5').on('click', function(event){ 
         $(".look").addClass('hide-left');
         $(".hide-left").removeClass('look');
         $('.item-text-5').addClass('look');
         $('.item-text-5').removeClass('hide-left', 'hide-right');   


         $(".nav-img").removeClass('active');
         $(this).addClass('active');  
     });
     
        
    // hide-right        
     
     $('.item-6').on('click', function(event){ 
         $(".look").addClass('hide-right');
         $(".hide-right").removeClass('look');
         $('.item-text-6').addClass('look');
         $('.item-text-6').removeClass('hide-right', 'hide-left'); 


         $(".nav-img").removeClass('active');
         $(this).addClass('active');    
     });

     $('.item-7').on('click', function(event){ 
         $(".look").addClass('hide-right');
         $(".hide-right").removeClass('look');
         $('.item-text-7').addClass('look');
         $('.item-text-7').removeClass('hide-right', 'hide-left');  


         $(".nav-img").removeClass('active');
         $(this).addClass('active');   
     });

     $('.item-8').on('click', function(event){ 
         $(".look").addClass('hide-right');
         $(".hide-right").removeClass('look');
         $('.item-text-8').addClass('look');
         $('.item-text-8').removeClass('hide-right', 'hide-left'); 


         $(".nav-img").removeClass('active');
         $(this).addClass('active');    
     });

     $('.item-9').on('click', function(event){ 
         $(".look").addClass('hide-right');
         $(".hide-right").removeClass('look');
         $('.item-text-9').addClass('look');
         $('.item-text-9').removeClass('hide-right', 'hide-left'); 


         $(".nav-img").removeClass('active');
         $(this).addClass('active');    
     });
     
     $('.item-10').on('click', function(event){ 
         $(".look").addClass('hide-right');
         $(".hide-right").removeClass('look');
         $('.item-text-10').addClass('look');
         $('.item-text-10').removeClass('hide-right', 'hide-left'); 


         $(".nav-img").removeClass('active');
         $(this).addClass('active');

     });
        
 
});

