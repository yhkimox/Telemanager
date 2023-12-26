(function($) {

    skel.breakpoints({
        xlarge: '(max-width: 1680px)',
        large: '(max-width: 1280px)',
        medium: '(max-width: 980px)',
        small: '(max-width: 736px)',
        xsmall: '(max-width: 480px)'
    });

    $(function() {

        var $window = $(window),
            $body = $('body'),
            $header = $('#header'),
            $banner = $('#banner');

        // Disable animations/transitions until the page has loaded.
        $body.addClass('is-loading');

        $window.on('load', function() {
            window.setTimeout(function() {
                $body.removeClass('is-loading');
            }, 100);
        });

        // Fix: Placeholder polyfill.
        $('form').placeholder();

        // Prioritize "important" elements on medium.
        skel.on('+medium -medium', function() {
            $.prioritize(
                '.important\\28 medium\\29',
                skel.breakpoint('medium').active
            );
        });

        // Menu.
        $('#menu')
            .append('<a href="#menu" class="close"></a>')
            .appendTo($body)
            .panel({
                delay: 500,
                hideOnClick: true,
                hideOnSwipe: true,
                resetScroll: true,
                resetForms: true,
                side: 'right'
            });

        // Header.
        if (skel.vars.IEVersion < 9)
            $header.removeClass('alt');

        if ($banner.length > 0 && $header.hasClass('alt')) {

            $window.on('resize', function() { $window.trigger('scroll'); });

            $banner.scrollex({
                bottom: $header.outerHeight(),
                terminate: function() { $header.removeClass('alt'); },
                enter: function() { $header.addClass('alt'); },
                leave: function() { $header.removeClass('alt'); $header.addClass('reveal'); }
            });
        }

        // Banner.
        var $banner = $('#banner');

        if ($banner.length > 0) {

            // IE fix.
            if (skel.vars.IEVersion < 12) {

                $window.on('resize', function() {

                    var wh = $window.height() * 0.60,
                        bh = $banner.height();

                    $banner.css('height', 'auto');

                    window.setTimeout(function() {

                        if (bh < wh)
                            $banner.css('height', wh + 'px');

                    }, 0);
                });

                $window.on('load', function() {
                    $window.triggerHandler('resize');
                });
            }

            // Video check.
            var video = $banner.data('video');

            if (video)
                $window.on('load.banner', function() {

                    // Disable banner load event (so it doesn't fire again).
                    $window.off('load.banner');

                    // Append video if supported.
                    if (!skel.vars.mobile && !skel.breakpoint('large').active && skel.vars.IEVersion > 9)
                        $banner.append('<video autoplay loop><source src="' + video + '.mp4" type="video/mp4" /><source src="' + video + '.webm" type="video/webm" /></video>');
                });

            // More button.
            $banner.find('.more')
                .addClass('scrolly');
        }

        // Tabs.
        $('.flex-tabs').each(function() {

            var t = jQuery(this),
                tab = t.find('.tab-list li a'),
                tabs = t.find('.tab');

            tab.click(function(e) {

                var x = jQuery(this),
                    y = x.data('tab');

                // Set Classes on Tabs
                tab.removeClass('active');
                x.addClass('active');

                // Show/Hide Tab Content
                tabs.removeClass('active');
                t.find('.' + y).addClass('active');

                e.preventDefault();
            });
        });

        // Scrolly.
        $('.scrolly').scrolly({
            offset: function() {
                return $header.height() - 2;
            }
        });
    });
})(jQuery);

//hj
// for modal
// 모달 열기 함수
function openModal() {
    document.getElementById('myModal').style.display = 'block';
}

// 모달 닫기 함수
function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

// 모달 외부 클릭 시 닫기
window.onclick = function(event) {
    if (event.target.className === 'modal') {
        closeModal();
    }
};

// 모달 닫기 버튼 클릭 시 닫기
document.getElementById('closeModalBtn').addEventListener('click', closeModal);

// 모달 열기
function openModal() {
    // Ajax를 사용하여 암호 변경 폼을 불러옴
    $.ajax({
        type: 'GET',
        url: '{% url "account:password_change" %}',
        success: function(data) {
            // 모달에 폼 내용 추가
            $('#myModal .modal-body').html(data);
            // 모달 열기
            $('#myModal').modal('show');
        }
    });
}

$(document).ready(function () {
    // 저장 버튼 클릭 시 alert 표시
    $('#submitBtn').click(function () {
        alert('저장되었습니다.');
    });
});
