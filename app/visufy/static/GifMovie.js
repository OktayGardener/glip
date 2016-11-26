function GifMovie(selector, gifArray, spotifyuri) {
  this.hook = $(selector);
  this.hook.append('<div id="loader"><span>0%</span><img src="static/loading.gif"></div>');
  this.hook.append('<div id="startspotify" style="display:none;"><iframe src="https://embed.spotify.com/?uri='+spotifyuri+'" width="300" height="80" frameborder="0" allowtransparency="true"></iframe></div>');

  this.hook.append('<div id="tools"><button id="fullscreen"></button></div>')
  this.fullscreen = false;
  this.hook.find("#fullscreen").click(this.toggleFullscreen.bind(this));
  this.toolstimer = 0;

  this.loader = this.hook.find("#loader");
  this.starter = this.hook.find("#startspotify");
  this.tools = this.hook.find("#tools");

  this.gifs = [];
  this.loaded = 0;
  this.nextGif = 0;
  this.currentGif = 0;
  for(var i in gifArray)  {
    var giftag = this.hook.append('<div id="jsgif-'+i+'" class="gif"><img id="gif-'+i+'" src="'+gifArray[i].url+'" class="gif"></img></div>');
    var gif = new SuperGif({
      gif: document.getElementById("gif-"+i),
      loop_mode: true,
      auto_play: false
    });
    this.gifs.push({gif: gif, duration: gifArray[i].duration });
    console.log("Trying to load " + i);
    gif.load(this.gifLoaded.bind(this));
  }
  console.log(this.gifs);
};

GifMovie.prototype.playNextGif = function() {
  console.log("Playing gif: " + this.nextGif);
  console.log(this.gifs);
  $("#jsgif-"+this.currentGif).hide();
  this.gifs[this.currentGif].gif.pause();
  if(this.nextGif < this.gifs.length) {
    $("#jsgif-"+this.nextGif).show();
    this.gifs[this.nextGif].gif.play();
    setTimeout(this.playNextGif.bind(this), this.gifs[this.nextGif].duration);
    this.currentGif = this.nextGif;
    this.nextGif++;
  }
}

GifMovie.prototype.gifLoaded = function() {
  this.loaded++;
  this.loader.find("span").html(Math.round((100 * this.loaded / this.gifs.length)) + "%");
  console.log("Loaded gifs: " + this.loaded);
  if(this.loaded == this.gifs.length) {
    this.loader.hide();
    this.starter.show();
    this.hook.mousemove(this.mouseMoved.bind(this));
    $(window).blur(this.play.bind(this) );
  }
}

GifMovie.prototype.play = function() {
  this.playNextGif();
  setTimeout(this.starter.hide, 100);
}

GifMovie.prototype.mouseMoved = function() {
  clearTimeout(this.toolstimer);
  this.toolstimer = setTimeout(this.toolFadeOut.bind(this), 2000);
  if(!this.tools.is(":visible")) {
    this.tools.fadeIn();
  }
}

GifMovie.prototype.toolFadeOut = function() {
  this.tools.fadeOut();
}

GifMovie.prototype.toggleFullscreen = function() {
  this.fullscreen = !this.fullscreen;
  if(this.fullscreen) {
    this.hook.collapsedCSS = {
      position: this.hook.css("position"),
      top: this.hook.css("top"),
      bottom: this.hook.css("bottom"),
      left: this.hook.css("left"),
      right: this.hook.css("right"),
      width: this.hook.css("width"),
      height: this.hook.css("height"),
      zIndex: this.hook.css("z-index")
    };
    this.hook.css({
      position: 'absolute',
      top: 0,
      bottom: 0,
      right: 0,
      left: 0,
      width: "auto",
      height: "auto",
      zIndex: 9999
    });
  } else {
    this.hook.css(this.hook.collapsedCSS);
  }
}
