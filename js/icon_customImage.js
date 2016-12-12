ymaps.ready(function () {
    var myMap = new ymaps.Map('map', {
            center: [48.700013, 31.311523],
            zoom: 6,
            controls: ['zoomControl']
        }, {
            searchControlProvider: 'yandex#search'
        }),
        myPlacemark = new ymaps.Placemark([50.51278, 30.821674], {
            hintContent: 'Украина, г.Бровары, ул.Оникиенко 77а',
            // balloonContent: 'Это красивая метка'
        }, {
            // Опции.
            // Необходимо указать данный тип макета.
            iconLayout: 'default#image',
            // Своё изображение иконки метки.
            iconImageHref: 'img/cust.png',
            // Размеры метки.
   

            iconImageSize: [40, 52],
            // Смещение левого верхнего угла иконки относительно
            // её "ножки" (точки привязки).
            iconImageOffset: [-20, -52]
        });
        myPlacemark1 = new ymaps.Placemark([46.964747, 32.078708], {
            hintContent: 'Украина, г. Николаев, ул. Электронная 81/24',
            // balloonContent: 'Это красивая метка'
        }, {
            // Опции.
            // Необходимо указать данный тип макета.
            iconLayout: 'default#image',
            // Своё изображение иконки метки.
            iconImageHref: 'img/cust.png',
            // Размеры метки.
            iconImageSize: [40, 52],
            // Смещение левого верхнего угла иконки относительно
            // её "ножки" (точки привязки).
            iconImageOffset: [-20, -52]
        });        

    myMap.geoObjects.add(myPlacemark);
    myMap.geoObjects.add(myPlacemark1);
});