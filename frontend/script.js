const imageInput =
    document.getElementById("imageInput");

const analyzeButton =
    document.getElementById("analyzeButton");

const preview =
    document.getElementById("preview");

const results =
    document.getElementById("results");

const loading =
    document.getElementById("loading");

const imageAnalysis =
    document.getElementById("imageAnalysis");

const objectsContainer =
    document.getElementById("objects");

const palette =
    document.getElementById("palette");

const temperature =
    document.getElementById("temperature");

const averageColor =
    document.getElementById("averageColor");


imageInput.addEventListener(
    "change",
    () => {

        const file =
            imageInput.files[0];

        if (!file) {
            return;
        }

        preview.src =
            URL.createObjectURL(file);

        results.classList.remove(
            "hidden"
        );
    }
);


analyzeButton.addEventListener(
    "click",
    async () => {

        const file =
            imageInput.files[0];

        if (!file) {

            alert(
                "Selecciona una imagen primero."
            );

            return;
        }


        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );


        loading.classList.remove(
            "hidden"
        );

        results.classList.remove(
            "hidden"
        );


        try {

            const response =
                await fetch(
                    "/analyze",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (data.error) {

                alert(data.error);

                return;
            }


            renderImageAnalysis(
                data.image
            );

            renderObjects(
                data.objects
            );

            renderColors(
                data.colors
            );


        } catch (error) {

            console.error(error);

            alert(
                "Ocurrió un error durante el análisis."
            );

        } finally {

            loading.classList.add(
                "hidden"
            );
        }
    }
);


function renderImageAnalysis(
    data
) {

    const metrics = [

        [
            "Resolución",
            `${data.width} × ${data.height}`
        ],

        [
            "Megapíxeles",
            data.megapixels
        ],

        [
            "Orientación",
            data.orientation
        ],

        [
            "Brillo",
            data.brightness_label
        ],

        [
            "Contraste",
            data.contrast_label
        ],

        [
            "Nitidez",
            data.sharpness_label
        ]

    ];


    imageAnalysis.innerHTML =
        metrics
            .map(
                ([label, value]) => `
                    <div class="analysis-item">
                        <span>${label}</span>
                        <strong>${value}</strong>
                    </div>
                `
            )
            .join("");
}


function renderObjects(
    objects
) {

    if (!objects.length) {

        objectsContainer.innerHTML =
            "<p>No se detectaron objetos.</p>";

        return;
    }


    objectsContainer.innerHTML =
        objects
            .map(
                object => `
                    <div class="object-item">
                        <span>
                            ${object.object}
                        </span>

                        <strong>
                            ${object.confidence}%
                        </strong>
                    </div>
                `
            )
            .join("");
}


function renderColors(
    data
) {

    temperature.textContent =
        data.temperature;

    averageColor.textContent =
        data.average_hex;


    palette.innerHTML =
        data.palette
            .map(
                color => `
                    <div class="color-item">

                        <div
                            class="color-swatch"
                            style="
                                background:
                                ${color.hex};
                            "
                        ></div>

                        <div class="color-info">

                            <strong>
                                ${color.name}
                            </strong>

                            <small>
                                ${color.hex}
                                ·
                                ${color.percentage}%
                            </small>

                        </div>

                    </div>
                `
            )
            .join("");
}