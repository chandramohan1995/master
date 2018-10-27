console.log('running');
var Twit = require('twit');
var config = require('./config');
var T = new Twit(config);

var stream = T.stream('user');
 

stream.on('follow',function(userfollowed){
   var name = userfollowed.source.name;
   var id = userfollowed.source.screen_name;
    tweetit('@'+name+' thanks for following,,see ya ');
});



function tweetit(txt){
    var r = Math.floor(Math.random()*100);
  var  tweet={
       status: txt +' '+ r
     }

 T.post('statuses/update',tweet, function(err, data, response) {
     if(err){
         console.log(err);
     }else{
         
    console.log('it worked');
  }
 });


}
