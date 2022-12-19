const guess_submit = document.getElementsByName("letter");

function usedLetters() {
  fetch("/fetch")
    .then((response) => response.json())
    .then(function (data) {
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
      let hidden = document.getElementById("hidden_word").textContent;
      if (hidden.includes("_") == false) {
        let win = document.getElementById("win-message");
        win.style.visibility = "visible";
        gsap.from(win, {
          duration: 1,
          opacity: 0,
        });
        setTimeout(() => {
          location.href = "/menu";
        }, 4000);
      }
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
              let lost = document.getElementById("lost-message");
              lost.style.visibility = "visible";
              gsap.from(lost, {
                duration: 1,
                opacity: 0,
              });
              setTimeout(() => {
                location.href = "/menu";
              }, 4000);
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
