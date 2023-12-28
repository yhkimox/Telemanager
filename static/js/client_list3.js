/* <!-- 전체 선택하는 버튼, 선택된 고객 삭제 버튼 클릭 시 경고창 뜨게 구현--> */
//<script>
document.addEventListener('DOMContentLoaded', function() { // 고객 정보 올리는 파트 체크박스 전체 선택 및 삭제 기능

    const selectAllCheckbox = document.getElementById('select-all');   //select-all 읽기

    selectAllCheckbox.addEventListener('change', function() {  // selectAll 체크박스의 상태가 변경될 때마다 실행
        const checkboxes = document.querySelectorAll('input[name="client_ids"]');  //모든 체크 된 요소 가져오기

        // selectAll 체크박스의 상태에 따라 모든 체크박스의 상태 변경
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });

    // 고객 삭제 버튼에 대한 이벤트 리스너
    const deleteButton = document.querySelector('button[type="submit"]');

    deleteButton.addEventListener('click', function(event) {
        const checkedCount = document.querySelectorAll('input[name="client_ids"]:checked').length;

        if (checkedCount > 0) {
            const confirmed = confirm('정말 선택된 고객을 삭제하시겠습니까?');
            if (!confirmed) {
                event.preventDefault(); // 폼 제출 중지
            }
        }
    });

});


document.addEventListener('DOMContentLoaded', function() { // 회사 파일 올리는 파트 체크박스 전체 선택 및 삭제 기능
    
    const selectAllCheckbox = document.getElementById('select-all2');   //select-all 읽기

    
    selectAllCheckbox.addEventListener('change', function() {  // selectAll 체크박스의 상태가 변경될 때마다 실행
        
        const checkboxes = document.querySelectorAll('input[name="file_ids"]');  //모든 체크 된 요소 가져오기

        // selectAll 체크박스의 상태에 따라 모든 체크박스의 상태 변경
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });

    //확인 메시지 표시
    const form = document.getElementById('file_form');
    form.addEventListener('submit', function(event) {
        const checkedCount = document.querySelectorAll('input[name="file_ids"]:checked').length;

        if (checkedCount > 0) {
            const confirmed = confirm('정말 선택된 파일을 삭제하시겠습니까?');
            if (!confirmed) {
                event.preventDefault(); // 폼 제출 중지
            }
        } 
    });
});

document.addEventListener('DOMContentLoaded', function() {//선택한 파일들을 프롬프트로 이동시키는 코드

    const outboundButton = document.querySelector('button > a[href="{% url 'client:selected_items' %}"]');
    outboundButton.addEventListener('click', function(event) {
        event.preventDefault(); 


        const selectedClientIds = Array.from(document.querySelectorAll('input[name="client_ids"]:checked')).map(checkbox => checkbox.value);
        const selectedFileIds = Array.from(document.querySelectorAll('input[name="file_ids"]:checked')).map(checkbox => checkbox.value);

        const urlParams = new URLSearchParams();
        urlParams.append('selected_clients', selectedClientIds.join(','));
        urlParams.append('selected_files', selectedFileIds.join(','));

        // 새로운 URL로 이동
        window.location.href = "{% url 'client:selected_items' %}?" + urlParams.toString();
    });
});

//</script>



/* <!-- 모달 관련 스크립트 --> */
//<script>
function openMockup() {
    const mockup = document.getElementById('mockup');
    mockup.style.display = 'block';
}

function closeMockup() {
    const mockup = document.getElementById('mockup');
    mockup.style.display = 'none';
}

// 모달 외부 클릭 시 닫기
window.onclick = function(event) {
    var modal = document.getElementById("myModal");
    if (event.target == modal) {
        closeModal();
    }
}

// 페이지 로드 시 목업 숨기기
document.addEventListener('DOMContentLoaded', function() {
    const mockup = document.getElementById('mockup');
    mockup.style.display = 'none';
});
//</script>

//<script>
function loadContentIntoMockup(url) {
    fetch(url)
    .then(response => response.text())
    .then(data => {
        const mockupContent = document.getElementById('mockup');
        mockupContent.innerHTML = data;
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

//</script>

/* <!-- 화면크기 동적 조정 --> */
//<script>
window.addEventListener('resize', function () {
    adjustTableWidth();
});

function adjustTableWidth() {
    var tableContainer = document.querySelector('.table-container');
    var table = document.querySelector('table');

    // 최소 폭 및 초기 설정 폭을 설정하고 필요에 따라 조절 가능
    var minWidth = 800;
    var initialWidth = 1200;

    // 현재 화면 폭 가져오기
    var windowWidth = window.innerWidth;

    // 테이블 폭을 조절
    table.style.width = (windowWidth >= minWidth) ? '100%' : initialWidth + 'px';
}

// 페이지 로드 시 초기 조절
window.addEventListener('load', function () {
    adjustTableWidth();
});
//</script>


/* 버튼 실험용 */
//<script>
document.querySelector('.my-button').addEventListener('click', function() {
    window.location.href = "{% url 'client:upload' %}";
});
//</script>
