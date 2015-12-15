console.log("Page analyzer running");

// Find all images
var images = $('img'); 

for (var i = 0; i < images.length ; i++) {
  var image = images[i];
  var extension = image.src.substr( (image.src.lastIndexOf('.') +1) );

  console.log(image.src, extension);

  switch(extension) {
        case 'jpg':
        case 'jpeg':
          console.log("Get exif");
      }

};



// Find all images with data attribute
//$('[data-myAttr!=""]'); 

//var StrippedString = document.all[0].outerHTML.replace(/(<([^>]+)>)/ig,"");
//console.log(StrippedString);
