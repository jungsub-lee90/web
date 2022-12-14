// 자바스크립트가 실행되면 최초 실행
init()
function init() {
    // 데이터 가져오기
    getData()
    // 이벤트 스탠바이
    setAddEvent()
    checkCnt()

}

// 초기 데이터셋을 비동기로 lending 상태로 만들고
async function getData() {
    //return await fetch('https://jsonplaceholder.typicode.com/todos/')
    let data = await fetch('https://jsonplaceholder.typicode.com/todos/')
        .then((response) => response.json())
        .then(data => data);
    let ul = document.querySelector('ul')
    for (let i = 0; i < data.length; i++) {
        if (i < 5) {
            ul.appendChild(createList(data[i].title, data[i].completed))
        }
    }
    checkCnt()

}
// li 생성
function createList(title, completed) {
    let li = document.createElement('li')
    // li에 괄호에 해당하는 clss css를 먹임
    li.classList.add('todo-item')
    li.innerHTML =
        `<div class="checkbox">${completed ? '✔' : ''}</div>
            <div class="todo" contenteditable='false'>${title}</div>
            <button class="delBtn">x</button>
            `
    // li 라는 요소 안에서 쿼리 셀렉터사용 더블클릭시 수정가능으로 변경
    li.querySelector('.todo').addEventListener('dblclick', ({ target }) => {
        target.contentEditable = 'true'
        target.focus()
        // keydown인 경우 키를 누르는 시점에 이미 editable false 가 먹혀 라인 생성 방지
        target.addEventListener('keydown', (event) => {
            event.key == 'Enter' ? target.contentEditable = 'false' : target.contentEditable = 'true';
        })
    })
    // checkbox 클릭 시, textContent 추가
    li.querySelector('.checkbox').addEventListener('click', ({ target }) => {
        target.textContent = '✔'
    })


    let delBtn = li.querySelector('button')
    // 버튼클릭시 삭제 이벤트 트리거링
    delBtn.addEventListener('click', removeParent)
    return li
}

// 이벤트 생성기, 값 입력 후 엔터치거나 버튼 클릭 시
function setAddEvent() {
    const input = document.querySelector('input')
    const buttons = document.querySelectorAll('button')

    input.addEventListener('keyup', (event) => {
        event.key == 'Enter' ? appendList() : '';
    })
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterList(btn.dataset.type)
        })
    })


}

//dataset type으로 넘어오는 값으로 분기처리
function filterList(type) {
    console.log(type)
    const lis = document.querySelectorAll('li')
    // 전체 출력
    if (type == 'all') {
        lis.forEach(li => {
            li.style.display = 'flex'
        })
        checkCnt()

    }
    //살아있는 얘들만 출력
    if (type == 'active') {
        lis.forEach(li => {
            if (li.children[1].style.color == "lightgray") {
                li.style.display = li.children[0].textContent == '✔' ? 'none' : 'flex'
            }
        })
        checkCnt()

    }
    // ✔ 클릭시 전체 완료 처리
    if (type == 'del') {
        delList()
    }
    //완료 된거 숨김처리
    if (type == 'clear_completed') {
        lis.forEach(li => {
            if (li.children[1].style.color == "lightgray"){
            li.style.display = li.children[0].textContent == '' ? 'flex' : 'none'
        }
        }
        )
        checkCnt()
    }
    if (type == 'completed') {
        lis.forEach(li => {
            if (li.children[0].textContent == '✔') {
                li.children[0].style.border = '2px solid darkgray'
                li.children[0].style.color = 'green'
                li.children[1].style.textDecoration = 'line-through'
                li.children[1].style.font = 'italic'
                li.children[1].style.color = 'lightgray'
            }

        })
    }
}
// 아이템 카운트
function checkCnt() {
    let lis = document.querySelectorAll('.todo-item')
    let itemCnt = document.querySelector('.left-items')
    let todos = document.querySelectorAll('.todo')
    todos.forEach(li => {
        //li.style.display = li.children[0].textContent == '' ? 'flex' : 'none'
        console.log(li.style)
    })
    
    if(lis.style.color == "lightgray"){
        itemCnt.innerHTML = `${lis.length} items left`
    }
}
// 할일 입력 후 엔터 입력시 할일 추가
function appendList() {
    const ul = document.querySelector('ul')
    const txtInput = document.querySelector('input')
    if (txtInput.value) {
        // li 생성 함수 호출
        ul.appendChild(createList(txtInput.value, false))
        checkCnt()
    }
    txtInput.value = ''

}


// 리스트 삭제
function removeParent({ target }) {
    target.parentElement.remove()
    checkCnt()
}

// 위에서 선언한 이벤트에 실행될 함수 
function delList() {
    if (confirm('완료처리 하실 겁니까?') == true) {
        let todo = document.querySelectorAll('.todo');
        for (let i = 0; i < todo.length; i++) {
            todo[i].style.textDecoration = 'line-through';
            todo[i].style.font = 'italic';
            todo[i].style.color = 'lightgray';
        }
        let chkbox = document.querySelectorAll('.checkbox');
        for (let i = 0; i < chkbox.length; i++) {
            chkbox[i].innerHTML = '✔'
            chkbox[i].style.border = '2px solid darkgray'
            chkbox[i].style.color = 'green'
        }
    }
}


