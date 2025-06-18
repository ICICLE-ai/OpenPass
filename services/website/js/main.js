var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
class Form {
    constructor() {
        this.formTwo = "                <div id=\"missonType\" class=\"input-group col-md-6\">\n                <div class=\"input-group-prepend\">\n                  <label class=\"input-group-text\" for=\"inputGroupSelect01\">Mission Type</label>\n                </div>\n                <select class=\"custom-select\" id=\"inputGroupSelect01\">\n                  <option selected>Please pick one of the following mission type</option>\n                  <option value=\"1\">One</option>\n                  <option value=\"2\">Two</option>\n                  <option value=\"3\">Three</option>\n                </select>\n              </div>\n              <div class=\"col-md-12\">\n                <input type=\"text\" class=\"form-control\" id=\"heatMapMetric\" placeholder=\"Metric of the Heat Map\"\n                  required=\"\" autocomplete=\"off\" name=\"heatMapMetric\">\n                <div class=\"valid-feedback\">\n                </div>\n              </div>\n  \n              <div class=\"col-md-12\">\n                <input type=\"text\" class=\"form-control\" id=\"missionDuration\" placeholder=\"Duration for this mission\"\n                  required=\"\" autocomplete=\"off\" name=\"missionDuration\">\n                <div class=\"valid-feedback\">\n                </div>\n              </div>\n              \n              <div class=\"col-12\">\n                 <button id=\"toStepThreeButton\" type=\"button\" class=\"btn navBtn\">\n                    Next step\n                  </button>\n              </div>";
    }
    getFormTwo() {
        return this.formTwo;
    }
}
class FormExtractor {
    constructor(formId) {
        this.map = new Map();
        const formo = document.querySelector(formId);
        for (let i = 0; i < formo.elements.length - 1; i++) {
            const element = formo.elements[i];
            this.map.set(element.name, element.value);
        }
    }
    checkForMissingElement() {
        const entries = this.map.entries();
        for (const entry of entries) {
            if (entry[0] == "faaCheck" || entry[0] == "acknowledgeCheck") {
                const faaCheck = document.querySelector("#checkFAACheck");
                const acknowledgeCheck = document.querySelector("#checkAcknowledgeCheck");
                if (!faaCheck.checked || !acknowledgeCheck.checked) {
                    return false;
                    break;
                }
            }
            if (entry[0] != "additionalInfo" && entry[1] == "") {
                console.log("missing elements: " + entry[0]);
                return false;
                break;
            }
        }
        return true;
    }
}
const sloganNInfo = document.getElementById('sloganNInfo');
const pic = document.getElementById('pic');
const picContent = pic.innerHTML;
const sloganNInfoContent = sloganNInfo.innerHTML;
if (window.innerWidth < 450) {
    pic.innerHTML = sloganNInfoContent;
    sloganNInfo.innerHTML = picContent;
}
const form = new Form();
function handle2StepTwoButtonClick() {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise((resolve, reject) => {
            const firstButton = document.getElementById('toStepTwoButton');
            firstButton.addEventListener('click', () => __awaiter(this, void 0, void 0, function* () {
                try {
                    const formExtractor = new FormExtractor("#demoForm");
                    if (formExtractor.checkForMissingElement()) {
                        document.getElementById("stageOne").style.opacity = "0.5";
                        document.getElementById("stageTwo").style.opacity = "1";
                        document.getElementById("stageThree").style.opacity = "0.5";
                        const result = form.getFormTwo();
                        const formDiv = document.getElementById('demoForm');
                        formDiv.innerHTML = result;
                        resolve('Passed step one!');
                    }
                    else {
                        console.log("fail to pass step one");
                    }
                }
                catch (error) {
                    console.error(error);
                    reject('Error!');
                }
            }));
        });
    });
}
function handle2StepThreeButtonClick() {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise((resolve, reject) => {
            const secondButton = document.getElementById('toStepThreeButton');
            secondButton.addEventListener('click', () => __awaiter(this, void 0, void 0, function* () {
                try {
                    const formExtractor = new FormExtractor("#demoForm");
                    if (formExtractor.checkForMissingElement()) {
                        document.getElementById("stageOne").style.opacity = "0.5";
                        document.getElementById("stageTwo").style.opacity = "0.5";
                        document.getElementById("stageThree").style.opacity = "1";
                        const result = form.getFormTwo();
                        const formDiv = document.getElementById('demoForm');
                        formDiv.innerHTML = "                <button type=\"button\" class=\"btn mx-auto homeBtn text-center\" style=\"width:50%; font-size: 1rem;\">\n                  Generate report\n                </button>";
                        resolve('Passed step two!');
                    }
                    else {
                        console.log("fail to pass step two");
                    }
                }
                catch (error) {
                    console.error(error);
                    reject('Error!');
                }
            }));
        });
    });
}
handle2StepTwoButtonClick().then(resultOne => {
    console.log(resultOne);
    handle2StepThreeButtonClick().then(resultTwo => {
        console.log(resultTwo);
    });
});
//# sourceMappingURL=main.js.map