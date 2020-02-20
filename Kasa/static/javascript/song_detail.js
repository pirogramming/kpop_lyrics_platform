//wrapper
Array.from(document.querySelectorAll("iframe")).forEach(function(a) {
  const r = a.width / a.height,
        reswrapper = document.createElement("div");

  reswrapper. classList.add("resvid", `${9 / 16 === r ? "alt" : 4 / 3 === r ? "old" : r === 1 && "square"}`),
  a.parentElement.insertBefore(reswrapper, a);
  reswrapper.appendChild(a)
})

//sticker
const youtubevid = document.getElementsByClassName("resvid"),
  notsticker = document.getElementsByClassName("not-sticker");

function sticker() {
  const sticker = document.getElementsByClassName("video-sticker")[0],
    scrolltop = window.scrollY;
  let offsettop;

  1 === youtubevid.length && 0 === notsticker.length && (
    offsettop = youtubevid[0].offsetTop,
    offsettop + youtubevid[0].offsetHeight > scrolltop && scrolltop + window.innerHeight > offsettop ? sticker.classList.remove("sticked") : sticker.classList.add("sticked")
  );
}

window.addEventListener("scroll", sticker);
document.addEventListener("DOMContentLoaded", function(){
  const iframe = document.getElementsByClassName("resvid")[0].getElementsByTagName("iframe")[0],
    wrapper = document.createElement("div"),
    remover = document.createElement("div");

  1 === youtubevid.length && 0 === notsticker.length && (
    wrapper.className = "video-sticker",
    remover.className = "video-sticker-remover",
    remover.addEventListener("click", function () {
      this.parentNode.removeAttribute("class")
    }),
    iframe.parentNode.insertBefore(wrapper, iframe),
    wrapper.appendChild(iframe),
    wrapper.appendChild(remover)
  ),
  sticker()
});


