$(document).ready(function () {

    $("#menu_list_user").click(function(){
        $("#list_user").load("list_user");
    });

    function geoFindMe() {

        function success(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            map.setCenter({ lat: latitude, lng: longitude });
            map.setZoom(18);
            var newLocation = new google.maps.LatLng(latitude, longitude);
            marker_current_location.setPosition(newLocation);

            marker_current_location.setAnimation(google.maps.Animation.BOUNCE);

        }

        function error() {
            alert('Tidak bisa mengambil posisi saat ini, hubungi admin..');
        }

        if (!navigator.geolocation) {

            alert('Geolocation is not supported by your browser');
        } else {
            //   alert('Sedang dicari');
            // status.textContent = 'Locating…';
            navigator.geolocation.getCurrentPosition(success, error);
        }

    }

    var checkTombolLocateExist = setInterval(function () {
        if ($("#tombol_locate").length) {

            $("#tombol_locate").click(function () {
                geoFindMe()
            });

            clearInterval(checkTombolLocateExist);
        }
    }, 100);



    var checkLocateExist = setInterval(function () {
        if ($(".gmnoprint.gm-bundled-control.gm-bundled-control-on-bottom").length) {

            $(".gmnoprint.gm-bundled-control.gm-bundled-control-on-bottom").append("<img id='tombol_locate' src='static/images/umkm-compas.png' >");

            clearInterval(checkLocateExist);
        }
    }, 100);

    function isNumberKey(evt) {
        var charCode = (evt.which) ? evt.which : evt.keyCode
        if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
        return true;
    }

    function validateEmail(email) {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }

    function validate() {
        var email = $("#email").val();

        if (validateEmail(email)) {
            return 'berhasil'
        } else {
            return 'bentuk emailnya harus ada @'
        }
    }


    $("#tombol_daftar").click(function () {

        if (validate() == 'berhasil') {

            $.post('daftar', $("#form_login").serialize(), function (data) {
                alert(data);
            });

        } else {
            alert(validate())
        }

    });

    $("#tombol_logout").click(function () {
        window.location = window.location['origin'] + "/logout";
    });

    $("#tombol_masuk").click(function () {

        if (validate() == 'berhasil') {

            $.post('masuk', $("#form_login").serialize(), function (data) {
                if (data == 'Berhasil') {
                    window.location.href = '/utama'
                }
                else {
                    alert(data);
                }
            });

        } else {
            alert(validate())
        }

    });

    $("#link_create_account").click(function () {
        $(".control").hide();
    });

    $("#place_id").on('keyup', function () {
        $(this).val();
    });

    $("#jenis_umkm").change(function () {
        var parent_id = $(this).val();
        // alert(parent_id);
        param = {
            parent_id: parent_id,
            parent_column: 'jenis_umkm_id',
            table: 'child_jenis_umkm',
            name: 'nama',
            select_name: 'jenis_umkm_detil',
            label: 'Jenis UMKM Detil :'
        }
        $("#dropdown_update").load('dropdown_update', param);
    });

    $("#tombol_lupa_password").click(function(){
        // $('html, body').css('overflowY', 'auto'); 
        $('html, body').css('pointer-events', 'none'); 
        if (validate() == 'berhasil') {

            $.post('lupa_password', $("#form_login").serialize(), function (data) {
                if (data == 'berhasil') {
                    alert('System telah berhasil mengirimkan email yang berisi password baru yang bisa di gunakan untuk login.');
                    $('html, body').css('pointer-events', 'auto'); 
                }
                else {
                    alert(data);
                    $('html, body').css('pointer-events', 'auto'); 
                }
            });


        } else {
            alert(validate())

        }

    });

    $("#jenis_umkm").on('change', function () {

        jenis_ukm = $("#jenis_umkm").val();

    });

});
