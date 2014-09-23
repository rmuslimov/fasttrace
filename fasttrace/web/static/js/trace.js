(function() {

    function setup_websocket() {
        var ws = new WebSocket("ws://" + window.location.host + "/ws");

        ws.onopen = function() {
            console.log("connected");
        };

        ws.onmessage = function(message) {
            var data = $.parseJSON(message.data);

            var filtered = $('[data-id='+data['kind']+'] input');
            console.log(filtered);
            if (filtered.length && filtered[0].checked) {
                var item = _.template($("#row-item").html())(data);
                $(item).hide().prependTo("#items-container").fadeIn(500);
            }
        };

        ws.onclose = function() {
            console.log('closing');
            setTimeout(setup_websocket, 3000);
        }
    }

    setup_websocket();
})();
