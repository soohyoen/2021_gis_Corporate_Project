const baseTemplate = `
<div class="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
    <div class="relative py-3 sm:mx-auto">
        <div class="leading-loose">
            <form class="max-w-7xl m-4 p-10 bg-white rounded shadow-xl">
                <p class="text-gray-800 font-medium mb-5 text-center">인테리어 계약서 분석</p>
                
                <p class="mt-8 text-gray-400 text-base font-medium">누락된 계약서 항목</p>
                <div class="mt-2 space-y-4">
                    {{> content}}
                </div>
            </form>
        </div>
    </div>
</div>
`;

export default Handlebars.compile(baseTemplate);