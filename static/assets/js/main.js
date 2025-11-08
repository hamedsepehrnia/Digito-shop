//////////////////////////////////// product image in single product
const mainImage = document.getElementById('mainImage');
const zoomBox = document.getElementById('zoomBox');
const zoomLens = document.getElementById('zoomLens');
function isMobile() {
    return window.innerWidth <= 768;
}
if (mainImage) {
  
  mainImage.addEventListener('mousemove', function(event) {
      if (isMobile()) return;
      const { left, top, width, height } = mainImage.getBoundingClientRect();
      const x = event.clientX - left;
      const y = event.clientY - top;
      const lensSize = 80;
      const lensX = Math.max(0, Math.min(x - lensSize / 2, width - lensSize));
      const lensY = Math.max(0, Math.min(y - lensSize / 2, height - lensSize));
      zoomLens.style.left = `${lensX}px`;
      zoomLens.style.top = `${lensY}px`;
      const zoomLevel = 2;
      zoomBox.style.backgroundImage = `url(${mainImage.src})`;
      zoomBox.style.backgroundSize = `${width * zoomLevel}px ${height * zoomLevel}px`;
      zoomBox.style.backgroundPosition = `-${lensX * zoomLevel}px -${lensY * zoomLevel}px`;
      zoomLens.classList.remove('hidden');
      zoomBox.classList.remove('hidden');
  });
}
if (mainImage) {
  mainImage.addEventListener('mouseleave', function() {
      zoomLens.classList.add('hidden');
      zoomBox.classList.add('hidden');
  });
}
function changeImage(element) {
    mainImage.src = element.src;
}
//////////////////////////////// Quantity input
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".quantity-container").forEach(container => {
    const input = container.querySelector("input[type='number']");
    const incrementButton = container.querySelector("button[data-action='increment']");
    const decrementButton = container.querySelector("button[data-action='decrement']");

    incrementButton.addEventListener("click", function () {
      let value = parseInt(input.value, 10);
      input.value = value + 1;
    });

    decrementButton.addEventListener("click", function () {
      let value = parseInt(input.value, 10);
      if (value > 1) {
        input.value = value - 1;
      }
    });
  });
});
////////////////////////////////////////// modal login register
document.querySelectorAll(".open-modal").forEach((button) => {
  button.addEventListener("click", () => {
    const modalId = button.getAttribute("data-modal");
    const modal = document.getElementById(modalId);
    const modalBox = modal.querySelector(".modal-box");

    modal.classList.remove("hidden");
    setTimeout(() => {
      modal.classList.add("opacity-100");
      modalBox.classList.remove("opacity-0", "scale-90");
    }, 10);
  });
});
document.querySelectorAll(".close-modal").forEach((button) => {
  button.addEventListener("click", () => {
    const modal = button.closest(".modal");
    const modalBox = modal.querySelector(".modal-box");
    modal.classList.remove("opacity-100");
    modalBox.classList.add("opacity-0", "scale-90");
    setTimeout(() => modal.classList.add("hidden"), 300);
  });
});
document.querySelectorAll(".modal").forEach((modal) => {
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      const modalBox = modal.querySelector(".modal-box");
      modal.classList.remove("opacity-100");
      modalBox.classList.add("opacity-0", "scale-90");
      setTimeout(() => modal.classList.add("hidden"), 300);
    }
  });
});
///////////////////////////////////////// verify 6 code
const inputElements = [...document.querySelectorAll('input.code-input')]
if (inputElements) {
  // window.addEventListener("load", () => inputElements[0].focus());
  inputElements.forEach((ele,index)=>{
    ele.addEventListener('keydown',(e)=>{
      if(e.keyCode === 8 && e.target.value==='') inputElements[Math.max(0,index-1)].focus()
    })
    ele.addEventListener('input',(e)=>{
      const [first,...rest] = e.target.value
      e.target.value = first ?? ''
      const lastInputBox = index===inputElements.length-1
      const didInsertContent = first!==undefined
      if(didInsertContent && !lastInputBox) {
        inputElements[index+1].focus()
        inputElements[index+1].value = rest.join('')
        inputElements[index+1].dispatchEvent(new Event('input'))
      }
    })
  })
}
function onSubmit(e){
  e.preventDefault()
  const code = inputElements.map(({value})=>value).join('')
  console.log(code)
}
///////////////////////////////////////// category header desktop
const categories = {
  cat1: [`
  <div>
                <a href="#" class="flex gap-x-2 items-center mb-5">
                  <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
                    گوشی موبایل
                  </div>
                  <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
                  </div>
                </a>
                <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سامسونگ
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      شیائومی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      آیفون
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      هاوائی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      اچ تی سی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      ال جی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سونی
                    </a>
                  </li>
                </ul>
                <a href="#" class="flex gap-x-2 items-center mb-5">
                  <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
                    گوشی موبایل
                  </div>
                  <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
                  </div>
                </a>
                <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سامسونگ
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      شیائومی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      آیفون
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      هاوائی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      اچ تی سی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      ال جی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سونی
                    </a>
                  </li>
                </ul>
              </div>
              <div>
                <a href="#" class="flex gap-x-2 items-center mb-5">
                  <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
                    گوشی موبایل
                  </div>
                  <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
                  </div>
                </a>
                <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سامسونگ
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      شیائومی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      آیفون
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      هاوائی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      اچ تی سی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      ال جی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سونی
                    </a>
                  </li>
                </ul>
                <a href="#" class="flex gap-x-2 items-center mb-5">
                  <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
                    گوشی موبایل
                  </div>
                  <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
                  </div>
                </a>
                <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سامسونگ
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      شیائومی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      آیفون
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      هاوائی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      اچ تی سی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      ال جی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سونی
                    </a>
                  </li>
                </ul>
              </div>
              <div>
                <a href="#" class="flex gap-x-2 items-center mb-5">
                  <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
                    گوشی موبایل
                  </div>
                  <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
                  </div>
                </a>
                <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سامسونگ
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      شیائومی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      آیفون
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      هاوائی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      اچ تی سی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      ال جی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سونی
                    </a>
                  </li>
                </ul>
                <a href="#" class="flex gap-x-2 items-center mb-5">
                  <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
                    گوشی موبایل
                  </div>
                  <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
                  </div>
                </a>
                <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سامسونگ
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      شیائومی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      آیفون
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      هاوائی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      اچ تی سی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      ال جی
                    </a>
                  </li>
                  <li>
                    <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
                      سونی
                    </a>
                  </li>
                </ul>
              </div>
  `],
  cat2: [`<div>
  <a href="#" class="flex gap-x-2 items-center mb-5">
    <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
      لپ تاپ
    </div>
    <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
    </div>
  </a>
  <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سامسونگ
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        شیائومی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        آیفون
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        هاوائی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        اچ تی سی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        ال جی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سونی
      </a>
    </li>
  </ul>
  <a href="#" class="flex gap-x-2 items-center mb-5">
    <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
      گوشی موبایل
    </div>
    <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
    </div>
  </a>
  <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سامسونگ
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        شیائومی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        آیفون
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        هاوائی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        اچ تی سی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        ال جی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سونی
      </a>
    </li>
  </ul>
</div>
<div>
  <a href="#" class="flex gap-x-2 items-center mb-5">
    <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
      گوشی موبایل
    </div>
    <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
    </div>
  </a>
  <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سامسونگ
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        شیائومی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        آیفون
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        هاوائی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        اچ تی سی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        ال جی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سونی
      </a>
    </li>
  </ul>
  <a href="#" class="flex gap-x-2 items-center mb-5">
    <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
      گوشی موبایل
    </div>
    <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
    </div>
  </a>
  <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سامسونگ
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        شیائومی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        آیفون
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        هاوائی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        اچ تی سی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        ال جی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سونی
      </a>
    </li>
  </ul>
</div>
<div>
  <a href="#" class="flex gap-x-2 items-center mb-5">
    <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
      گوشی موبایل
    </div>
    <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
    </div>
  </a>
  <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سامسونگ
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        شیائومی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        آیفون
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        هاوائی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        اچ تی سی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        ال جی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سونی
      </a>
    </li>
  </ul>
  <a href="#" class="flex gap-x-2 items-center mb-5">
    <div class="w-fit min-w-fit text-primary-500 text-sm hover:text-primary-700 transition">
      گوشی موبایل
    </div>
    <div class="w-full h-0.5 border-t border-dashed border-primary-500/30">
    </div>
  </a>
  <ul class="pr-4 flex flex-col gap-y-3 text-xs mb-3">
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سامسونگ
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        شیائومی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        آیفون
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        هاوائی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        اچ تی سی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        ال جی
      </a>
    </li>
    <li>
      <a href="#" class=" text-zinc-500 hover:text-zinc-700 transition">
        سونی
      </a>
    </li>
  </ul>
</div>`],
  cat3: ["زیرمجموعه ۳-۱", "زیرمجموعه ۳-۲", "زیرمجموعه ۳-۳", "زیرمجموعه ۳-۴"],
  cat4: ["زیرمجموعه ۴-۱"],
  cat5: ["زیرمجموعه ۵-۱", "زیرمجموعه ۵-۲"],
  cat6: ["زیرمجموعه ۵-۱", "زیرمجموعه ۵-۲"],
  cat7: ["زیرمجموعه ۵-۱", "زیرمجموعه ۵-۲"],
  cat8: ["زیرمجموعه ۵-۱", "زیرمجموعه ۵-۲"],
};
// defult show first category
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".category-item").forEach(item => item.classList.remove("bg-gradient-to-l","from-zinc-100","to-transparent"));
  if (document.querySelector("[data-category='cat1']")) {
    document.querySelector("[data-category='cat1']").classList.add("bg-gradient-to-l","from-zinc-100","to-transparent");
  }
});
document.querySelectorAll(".category-item").forEach(item => {
  item.addEventListener("mouseenter", (e) => {
    const category = e.target.getAttribute("data-category");
    const subContainer = document.getElementById("subcategory-container");
    // change color selected category
    document.querySelectorAll(".category-item").forEach(item => item.classList.remove("bg-gradient-to-l","from-zinc-100","to-transparent"));
    e.target.classList.add("bg-gradient-to-l","from-zinc-100","to-transparent");
    // show sub category
    subContainer.innerHTML = categories[category]
      ? categories[category].map(sub => sub).join("")
      : "<p class='text-gray-400'>زیرمجموعه‌ای وجود ندارد</p>";
  });
});
// close category mouse leave
const dropdownMenu = document.getElementById("dropdown-menu");
if (document.getElementById("dropdown-menu")) {
  dropdownMenu.addEventListener("mouseleave", () => {
    dropdownMenu.classList.remove("opacity-100", "visible");
    dropdownMenu.classList.add("opacity-0", "invisible");
  });
}
//////////////////////////////////////////// open and close mobile navbar
document.addEventListener("DOMContentLoaded", function () {
  const menu = document.getElementById("mobile-menu");
  const overlay = document.getElementById("overlay");
  const openBtn = document.querySelector(".menu-mobile");
  function openMenu() {
    menu.classList.remove("translate-x-full");
    overlay.classList.remove("hidden");
    overlay.classList.add("opacity-100");
  }
  function closeMenu() {
    menu.classList.add("translate-x-full");
    overlay.classList.add("hidden");
    overlay.classList.remove("opacity-100");
  }
  openBtn.addEventListener("click", openMenu);
  overlay.addEventListener("click", closeMenu);
});
//////////////////////////////////////////// open and close menu/submenu mobile
document.addEventListener("DOMContentLoaded", function () {
  const menuToggles = document.querySelectorAll(".menu-toggle");
  menuToggles.forEach((toggle) => {
    toggle.addEventListener("click", function () {
      const submenu = this.nextElementSibling;
      const icon = this.querySelector("img");
      if (submenu.classList.contains("hidden")) {
        submenu.classList.remove("hidden");
        icon.classList.add("rotate-180");
      } else {
        submenu.classList.add("hidden");
        icon.classList.remove("rotate-180");
      }
    });
  });
});
/////////////////////////////////////////// progressBar
window.addEventListener("scroll", function () {
  let scrollTop = document.documentElement.scrollTop; // میزان اسکرول شده
  let scrollHeight =
    document.documentElement.scrollHeight -
    document.documentElement.clientHeight; // ارتفاع کل صفحه
  let scrollPercentage = (scrollTop / scrollHeight) * 100; // محاسبه درصد اسکرول
  document.getElementById("progressBar").style.width = scrollPercentage + "%"; // تغییر عرض نوار
});
//////////////////////////////// loading
window.addEventListener("load", function () {
  const loadingScreen = document.getElementById("loading");
  setTimeout(() => {
    loadingScreen.classList.add("opacity-0");
  }, 500);
  setTimeout(() => {
    loadingScreen.classList.add("hidden");
  }, 1000);
});
//////////////////////////////// btn go to top
document.getElementById("btn-back-to-top").addEventListener("click", function() {
  window.scrollTo({
      top: 0,
  });
});
/////////////////////////////// faq
function toggleFAQ(id) {
  const content = document.getElementById(`faq${id}`);
  const icon = content.previousElementSibling.querySelector('.icon');
  if (content.classList.contains('open')) {
      content.classList.remove('open');
      icon.textContent = '+';
  } else {
      content.classList.add('open');
      icon.textContent = '-';
  }
}
/////////////////////////////// rules
function toggleRules(id) {
  const content = document.getElementById(`rules${id}`);
  const icon = content.previousElementSibling.querySelector('.icon');
  if (content.classList.contains('open')) {
      content.classList.remove('open');
      icon.textContent = '+';
  } else {
      content.classList.add('open');
      icon.textContent = '-';
  }
}
/////////////////////////////// price filter
let priceFilter = document.querySelectorAll("#shop-price-slider"),
  priceMinFilter = document.querySelectorAll("#shop-price-slider-min"),
  priceMaxFilter = document.querySelectorAll("#shop-price-slider-max");
  priceFilter.forEach((e) => {
    noUiSlider.create(e, {
      cssPrefix: "range-slider-",
      start: [0, 1e8],
      direction: "rtl",
      margin: 1,
      connect: !0,
      range: { min: 0, max: 1e8 },
      format: {
        to: function (e) {
          return e.toLocaleString("en-US", {
            style: "decimal",
            maximumFractionDigits: 0,
          });
        },
        from: function (e) {
          return parseFloat(e.replace(/,/g, ""));
        },
      },
    }),
      e.noUiSlider.on("update", function (e, t) {
        t
          ? priceMaxFilter.forEach((a) => {
              a.innerHTML = e[t];
            })
          : priceMinFilter.forEach((a) => {
              a.innerHTML = e[t];
            });
      });
  })
/////////////////////////////// copy link page to clipboard
function copyToClipboard(event) {
  event.preventDefault();
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(() => {}).catch(err => {});
}
//////////////////////////////////// open filter in search products
if (document.getElementById("mobile-filter")) {
  const filters = document.getElementById("mobile-filter");
  const openFilter = document.querySelector(".filter-mobile");
  const closeFilter = document.getElementById("closeFilter");
  function openMenu() {
    filters.classList.remove("translate-y-full");
  }
  function closeMenu() {
    filters.classList.add("translate-y-full");
  }
  openFilter.addEventListener("click", openMenu);
  closeFilter.addEventListener("click", closeMenu);
}