function GifMovie(selector, data) {
  console.log(data);
  this.hook = $(selector);

  this.hook.html("");
  this.hook.show();

  this.hook.append('<div id="loader"><span>0%</span><img src="static/loading.gif"></div>');
  this.hook.append('<div id="startspotify" style="display:none;"><iframe src="https://embed.spotify.com/?uri='+data.uri+'" width="300" height="80" frameborder="0" allowtransparency="true"></iframe></div>');

  this.hook.append('<div id="messages"></div>');
  this.messageTimer = 0;

  this.hook.append('<div id="tools"><div id="songinfo">' + data.artist + ' - ' + data.title + '</div><button id="fullscreen"></button></div>')
  this.fullscreen = false;
  this.hook.find("#fullscreen").click(this.toggleFullscreen.bind(this));
  this.toolstimer = 0;

  this.hook.append('<img id="gifview" style="display:none;">');

  this.message = this.hook.find("#messages");
  this.view = this.hook.find("#gifview");
  this.loader = this.hook.find("#loader");
  this.starter = this.hook.find("#startspotify");
  this.tools = this.hook.find("#tools");

  this.gifs = data.gifs;
  this.loaded = 0;
  this.nextGif = 0;
  this.currentGif = 0;
  if(this.gifs.length > 0) {
    for(var i in this.gifs)  {
      var img = $("<img />").attr("src", this.gifs[i].url);
      img.on("load", this.gifLoaded.bind(this));
      console.log("Preloading image: " + i);
    }
  } else {
    console.log(this);
    this.loader.hide();
    this.msg("Could not get the lyrics.")
  }
};

GifMovie.prototype.playNextGif = function() {
  console.log("Playing gif: " + this.nextGif);
  if(this.nextGif < this.gifs.length) {
    this.view.attr("src", this.gifs[this.nextGif].url);
    setTimeout(this.playNextGif.bind(this), this.gifs[this.nextGif].duration);
    this.currentGif = this.nextGif;
    this.nextGif++;
  } else {
    this.view.hide();
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
  this.view.show();
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

GifMovie.prototype.msg = function(msg, timer) {
  clearTimeout(this.messageTimer);
  this.message.html(msg);
  this.message.show();
  if(typeof timer !== 'undefined')
    this.messageTimer = setTimeout(this.message.hide, timer);
}
