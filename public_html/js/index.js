import * as Vue from '/js/vue.esm-browser.js';
const { createApp, ref, reactive } = Vue;
createApp({
    setup() {
        const title = ref(''),
        content = ref(''),
        image = reactive({}),
        posting = ref(false);
        async function postContent() {
            posting.value = true;
            const body = { title: title.value, content: content.value };
            if (image.name) {
                body.image = image;
            }
            try {
                await fetch('/post', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(body)
                });
            } finally {
                posting.value = false;
            }
        }
        function setImage(e) {
            if (e.target.files.length) {
                const imageFile = e.target.files[0];
                if (/^image\/*/.test(imageFile.type)) {
                    const reader = new FileReader();
                    reader.onload = () => {
                        image.name = imageFile.name;
                        image.content = reader.result;
                    };
                    reader.readAsDataURL(imageFile);
                    return;
                }
            }
            delete image.name;
            delete image.content;
        } 
        return { title, content, setImage, postContent };
    }
}).mount('#app');