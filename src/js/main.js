function main() {

    setTimeout(function(){console.log("Ready")}, 10 * 1000)
}

// $(document).ready(main);

function trawl() {
    var username = $(".username").val()
    if (! username) {
        console.log("Please enter a username")
        $('.username').addClass("missing-username");
    } else {
        $('.username').removeClass("missing-username");
        console.log("Trawling Last.fm data for username: " + username)
        get_raw(username)
        console.log("Async shit")
    }
}

function Listen(artist, album, track, date) {
    this.artist = artist
    this.album = album
    this.track = track
    this.date = date
}

function get_raw(username) {
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", "test.xml");
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                xmlDoc = $.parseXML(allText)
                $xml = $(xmlDoc)
                var listens = []
                $xml.find("lfm").find("recenttracks").find("track").each(function(){
                    var listen = new Listen($(this).find("artist").text(),
                               $(this).find("album").text(),
                               $(this).find("name").text(),
                               new Date($(this).find("date").text()).getTime())
                    listens.push(listen)
                })
                console.log(listens.length);
                for (listen of listens) {
                    console.log(new Date(listen.date) + ": " + listen.artist + " - " + listen.track)
                }
            }
        }
    }
    rawFile.send(null);
}

