var audio1 = new Audio('happy.mp3'); //I defined all the variables outside so i could know which one is playing.
var audio2 = new Audio('sad.mp3');
var audio3 = new Audio('angry.mp3');
var audio4 = new Audio('afraid.mp3');
var audio5 = new Audio('surprised.mp3');
function isPlaying(audelem){return !audelem.paused;} //When is paused return true, so the inverse when is playing return true.

var feliz = ["happy/happy1.jpg", "happy/happy2.jpg", "happy/happy3.jpg", "happy/happy4.jpg", "happy/happy5.jpg", "happy/happy6.jpg"]
function get_random_feliz(){
  random_index = Math.floor(Math.random() * feliz.length); //Randomize a number in the range of 1 up to the lenght of the list
  selected = feliz[random_index]; //Chooses an element of the array using random index.
  document.getElementById('f').src = selected; //replace the source code of the image with the randomly selected one
  if (isPlaying(audio1) == false && isPlaying(audio2) == false && isPlaying(audio3) == false && isPlaying(audio4) == false && isPlaying(audio5) == false){
    audio1.play(); //If non of the other audios is playing, play this audio (i created a function to know if a audio is playing)
  }
}
var triste = ["sad/sad1.jpg", "sad/sad2.jpg", "sad/sad3.jpg", "sad/sad4.jpg", "sad/sad5.jpg", "sad/sad6.jpg", "sad/sad7.jpg"]
function get_random_triste(){
  random_index = Math.floor(Math.random() * triste.length);
  selected = triste[random_index];
  document.getElementById('f').src = selected;
  if (isPlaying(audio1) == false && isPlaying(audio2) == false && isPlaying(audio3) == false && isPlaying(audio4) == false && isPlaying(audio5) == false){
    audio2.play();
  }
}
var enojado = ["angry/angry1.jpg", "angry/angry2.jpg", "angry/angry3.jpg", "angry/angry4.jpg", "angry/angry6.jpg"]
function get_random_enojado(){
  random_index = Math.floor(Math.random() * enojado.length);
  selected = enojado[random_index];
  document.getElementById('f').src = selected;
  if (isPlaying(audio1) == false && isPlaying(audio2) == false && isPlaying(audio3) == false && isPlaying(audio4) == false && isPlaying(audio5) == false){
    audio3.play();
  }
}
var asustado = ["afraid/afraid1.jpg", "afraid/afraid2.jpg", "afraid/afraid3.jpg", "afraid/afraid4.jpg", "afraid/afraid5.jpg", "afraid/afraid6.jpg"]
function get_random_asustado(){
  random_index = Math.floor(Math.random() * asustado.length);
  selected = asustado[random_index];
  document.getElementById('f').src = selected;
  if (isPlaying(audio1) == false && isPlaying(audio2) == false && isPlaying(audio3) == false && isPlaying(audio4) == false && isPlaying(audio5) == false){
    audio4.play();
  }
}
var sorprendido = ["surprised/surprised1.jpg", "surprised/surprised2.jpg", "surprised/surprised3.jpg", "surprised/surprised4.jpg"]
function get_random_sorprendido(){
  random_index = Math.floor(Math.random() * sorprendido.length);
  selected = sorprendido[random_index];
  document.getElementById('f').src = selected;
  if (isPlaying(audio1) == false && isPlaying(audio2) == false && isPlaying(audio3) == false && isPlaying(audio4) == false && isPlaying(audio5) == false){
    audio5.play();
  }
}
