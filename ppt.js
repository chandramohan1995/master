var pptx = new PptxGenJS();
//$('#ver').html('<h5>'+pptx.version+'</h5>');

// Simple Slide
function doDemo() {
	var slide = pptx.addNewSlide();
	canvas = document.getElementsBYTagname("canvas")
    var img = canvas.toDataURL("image/png")
   let boxHeight = 0.7, boxWidth = 0.7, paddingV = 0, paddingH = 0;
//draw a box of specified dimension
   slide.addShape(pptx.shapes.RECTANGLE, { x: 0.5, y: 0.5, w: 0.7, h: 0.7, line: 'BEB5AF' });
   let newImgHeight = boxHeight;
   let newImgWidth = boxWidth;
   let sampleImage = img;
   if (sampleImage.height >= sampleImage.width) {
  // if height is more we need to shrink the width to fit the box
   newImgWidth = (sampleImage.width * boxHeight) / sampleImage.height;
   paddingH = (0.7 - newWidth) * 0.5;
 }
 else {
  // if width is more we need to shrink the height to fit the box
  newImgHeight = (sampleImage.height * boxWidth) / sampleImage.width; paddingV = (0.7 - imageHeight) * 0.5;
}
slide.addImage({ data: `image/png;base64,img}`, x: 0.5 + paddingH, y: 0.5 + paddingV, w: newImgWidth, h: newHeight });
pptx.save();
}
