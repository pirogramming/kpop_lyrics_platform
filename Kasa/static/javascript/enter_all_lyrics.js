var eng_lyrics = document.getElementById(('all_eng'));
var add_eng = document.getElementById(('add_eng'))

add_eng.addEventListener('click', function() {
    if (eng_lyrics.style.display === 'none') {
        eng_lyrics.style.display = 'block';

    } else {
        eng_lyrics.style.display = 'none';
    }
});

var rom_lyrics = document.getElementById(('all_rom'));
var add_rom = document.getElementById(('add_rom'))

add_rom.addEventListener('click', function(){
    if (rom_lyrics.style.display === 'none') {
        rom_lyrics.style.display = 'block';
    } else {
        rom_lyrics.style.display = 'none';
    }

});