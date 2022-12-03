// gsap.to(".guess", { y: 100, duration: 1 });
// gsap.from(".plank2", { y: "-100%", duration: 2, ease: "bounce" });
// gsap.from(".plank1", { y: "-100%", duration: 2, ease: "bounce" });
// gsap.from(".rope", { y: "-100%", duration: 2, ease: "bounce" });
// gsap.from(".plank3", { y: "-100%", duration: 2, ease: "bounce" });
// gsap.from(".head", { x: "300%", rotation: 1000, duration: 2, ease: "step" });
// gsap.from(".body", { y: "-100%", duration: 2, ease: "step" });
// gsap.from(".larm", { y: "100%", duration: 2, ease: "step" });
// gsap.from(".rarm", { y: "-100%", duration: 2, ease: "step" });
// gsap.from(".rleg", { x: "100%", duration: 2, ease: "circ.out" });
// gsap.from(".lleg", { x: "-100%", duration: 2, ease: "step" });

// guess_submit.addEventListener("click", function (e) {
//   gsap.from(".head", { x: "300%", rotation: 1000, duration: 2, ease: "step" });
//   guess_submit.style.display = "none";
// });
const guess_submit = document.getElementsByName("letter");
// let hidden_word = document.getElementById("hidden_word").textContent;
// function getOccurrence() {
//   hidden_word.split("");
// }
// console.log(getOccurrence());
console.log(guess_submit[2].value);

function usedLetters() {
  fetch("/fetch")
    .then((response) => response.json())
    .then(function (data) {
      console.log(data[0]);
      for (let i = 0; i < guess_submit.length; i++) {
        if (data[0].includes(guess_submit[i].value)) {
          gsap.to(guess_submit[i], { y: -100, duration: 0.7, opacity: 0 });
          setTimeout(() => {
            guess_submit[i].style.visibility = "hidden";
          }, 700);
        }
      }
    });
}

usedLetters();

function hangMan() {
  fetch("/fetch")
    .then((response) => response.json())
    .then(function (data) {
      console.log(data[1]);
      if (data[1] > 0) {
        for (let i = 1; i <= data[1]; i++) {
          let body_part = document.getElementById(`${i}`);
          body_part.style.visibility = "visible";
          if (i != data[1]) {
            gsap.from(body_part, {
              duration: 1,
              opacity: 0,
            });
          } else if (i == data[1] && data[2] == 0) {
            gsap.from(body_part, {
              x: `${Math.floor(Math.random() * 200) + 1}%`,
              y: `${Math.floor(Math.random() * 200) + 1}%`,
              rotation: 360,
              duration: 2,
              ease: "bounce",
              opacity: 0,
            });
            if (data[1] == 10) {
              setTimeout(() => {
                alert("You've DIEDED ;/");
                location.href = "/menu";
              }, 1000);
            }
          } else {
            gsap.from(body_part, {
              duration: 1,
              opacity: 0,
            });
          }
        }
      }
    });
}

hangMan();
