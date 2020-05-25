//create a constructor function to be used in the end

function Suggest() {
    othis = this;//save this for future
    this.xhr = new XMLHttpRequest();
    this.moviepart = null;

    this.div = null;

    //create a timer(to decide when to go to server)
    this.timer = null;

    this.getMovie = function () {
        if (this.timer) {
            clearTimeout(this.timer);
        }
        //get ready to go to server in 1 second
        //if the user types something before 1 second, this function will be called and the timer is cancelled before registering a new one
        //if the user keeps quite for more than 1 second the fetchMovie function is called anyways

        this.timer = setTimeout(this.fetchMovies, 1000);
    }
    //function to check if we need to go
    this.fetchMovies = function () {
        //Check if movie textbox is blank. This can happen if the user repeatedly used the backspace to clear the box
        othis.moviepart = document.getElementById("searchbar");
        if (othis.moviepart.value == "") {
            othis.div = document.getElementById("container");
            othis.div.innerHTML = "";
            othis.div.style.display = "none";
        }
        else {
            //BUild the key to search in localStorage
            key = "suggest.php?moviepart=" + othis.moviepart.value;
            if (localStorage[key])//We need to check in cache
            {
                //alert(localStorage[key]);
                //if we have it in the cache, show the movie list corresponding to this movie;;;how to check, go to networks and make sure GET isnt there
                //alert(localStorage[key]);
                othis.div = document.getElementById("container");
                othis.div.innerHTML = "";
                movielist = JSON.parse(localStorage[key]);
                for (i = 0; i < movielist.length; i++) {
                    newdiv = document.createElement("div");
                    newdiv.innerHTML = movielist[i];
                    newdiv.className = "suggest";
                    othis.div.appendChild(newdiv);

                    //now register for the click
                    newdiv.onclick = othis.setMovie;
                }
                //show the container
                othis.div.style.display = "block";
            }
            else//no choice but to go to the server
            {
                othis.xhr.onreadystatechange = othis.processRes;//window will call this function on xhr otherwise control is with window only
                othis.xhr.open("GET", "suggest.php?moviepart=" + othis.moviepart.value, true);
                othis.xhr.send();
            }
        }
    }//end of fetch movies
    this.processRes = function () {
        //alert("suo")
        if (this.readyState == 4 && this.status == 200) {
            //First parse the json sent by the server
            //cleanup the div before populating new movies
            //alert(this.responseURL);
            movies = JSON.parse(this.responseText);
            othis.div = document.getElementById("container");
            othis.div.innerHTML = "";
            //alert(this.responseText);
            if (movies.length == 0) {
                //Server could not find any suggestions

                othis.div.style.display = "none";
            }
            else//We have some suggestions
            {
                //alert(movies)
                for (i = 0; i < movies.length; i++) {
                    newdiv = document.createElement("div");
                    newdiv.innerHTML = movies[i];
                    newdiv.className = "suggest";
                    othis.div.appendChild(newdiv);

                    //now register for the click
                    newdiv.onclick = othis.setMovie;
                }
                //show the container
                othis.div.style.display = "block";

                //save to localStorage for later use
                localStorage[this.responseURL] = this.responseText;
            }
        }
    }
    //when user selects a movie from the list, set into the textbox and clear the container div
    this.setMovie = function () {
        othis.moviepart.value = this.innerHTML;
        othis.div.innerHTML = "";
        othis.div.style.display = "none";
    }

}

obj = new Suggest();