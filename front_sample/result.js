import baseTemplate from './templates/base.template.js'
import itemTemplate from './templates/item.template.js'

Handlebars.registerPartial("content", itemTemplate);

const articleTitle = ['목적', '계약문서', '계약서 제공․설명 의무', '계약내용', '"시공업자"의 의무',
                    '"소비자"의 의무', '지연배상', '계약해제 및 위약금', '현장대리인의 배치',
                    '자재의 검사', '공사변경', '양도양수', '하자보수', '부적합한 공사', '불가항력에 의한 손해',
                    '안전관리', '응급조치', '손해배상책임', '분쟁의 해결', '관할법원'];
const notIncludeAritcle = [1, 2];
const data = {"item": []};
notIncludeAritcle.forEach(async val => {
    let articleTemplate = await import(`./templates/article_${val}.template.js`);
    data['item'].push({
        'title': articleTitle[val-1],
        'item_detail': new Handlebars.SafeString(articleTemplate.default()),
    });

    document.getElementById('root').innerHTML = baseTemplate(data);
});