const template = `
<ol class="list-decimal list-outside pl-4">
    <li>계약문서는 인테리어(리모델링) 도급계약서, 상세 견적서, 공정표로 구성되며, 상호 보완의 효력을 가진다.</li>
    <li>이 조건이 정하는 바에 의하여 계약당사자간에 행한 통지문서는 계약문서로서의 효력을 가진다.</li>
    <li>도급계약서, 상세 견적서, 공정표에 기입된 사항 중 변경된 사항이 있다면 추가, 정정 사항을 반영하여 재출력 후 제출한다.</li>
</ol>
`;

export default Handlebars.compile(template);