<!DOCTYPE html>
<html>

    <head>
        <title>GoGroups | Meetings made easy.</title>
        <meta name = "viewport" content = "width=device-width, minimum-scale=1, maximum-scale=1">
        
        <!-- META -->
        <meta charset = "utf-8">
        
        <!-- Loading Bootstrap -->
        <link href="flat-ui-master/css/bootstrap.css" rel="stylesheet">
        <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css" rel="stylesheet">
    
        <!-- Loading Flat UI -->
        <link href="flat-ui-master/css/flat-ui.css" rel="stylesheet">
        <link rel="shortcut icon" href="../../../../images/favicon.ico">


        <!-- CSS -->
        <link rel = "stylesheet" media = "screen" href = "_css/common.css" />
        
        <!-- JS -->
        <script src = "_lib/jquery-1.4.min.js"></script>
        <script src = "_lib/jquery.easing-1.3.js"></script>
        
        <!-- iosSlider plugin -->
        <script src = "_src/jquery.iosslider.js"></script>
        
        <script type="text/javascript">
            $(document).ready(function() {
                
                $('.iosSlider1').iosSlider({
                    snapToChildren: true,
                    desktopClickDrag: true
                });
                
                $('.iosSlider2').iosSlider({
                    snapToChildren: true,
                    desktopClickDrag: true
                });
                
                $('.toggle').bind('click', function() {

                    if($('.main').hasClass('sliderHidden')) {
                        
                        $('.main').removeClass('sliderHidden');
                    
                    } else {
                    
                        $('.main').addClass('sliderHidden');
                    
                    }
                    
                    /* call to rerender iosSlider */
                    $('.iosSlider1').iosSlider('update');
                
                });
                
            }); 
        </script>
                
    </head>
    
    <body>
        <h4>Monday Availability</h4>
        <div class = 'main '>
            <div class = 'slider1Container'>
                <div class = 'iosSlider1' style="float:left">
                    <div class = 'slider'>
                        <div class = 'item item1 odd-green'><h5>8:00am - 8:30am</h5></div>
                        <div class = 'item item2 odd-red' ><h5>BUSY</h5></div>
                    </div>
                </div>  
                <div class = 'iosSlider1' style="float:right">
                    <div class = 'slider'>
                        <div class = 'item item1 odd-green'><h5>8:30am - 9:00am</h5></div>
                        <div class = 'item item2 odd-red'><h5>BUSY</h5></div>                   
                    </div>
                </div>      
                <div class = 'iosSlider1' style="float:left">
                    <div class = 'slider'>
                        <div class = 'item item1 even-green'><h5>9:00am - 9:30am</h5></div>
                        <div class = 'item item2 even-red'><h5>BUSY</h5></div>                  
                    </div>
                </div>  
                <div class = 'iosSlider1' style="float:right">
                    <div class = 'slider'>
                        <div class = 'item item1 even-green'><h5>9:30am - 10:00am</h5></div>
                        <div class = 'item item2 even-red'><h5>BUSY</h5></div>                  
                    </div>
                </div>      
            </div>      
        </div>          
    </body>
    
</html>