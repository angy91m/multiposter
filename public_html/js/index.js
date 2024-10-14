const app = new Vue({
    el: '#app',
    data: {
        title: '',
        content: '',
        image: {},
        posting: false
    },
    methods: {
        async postContent() {
            this.posting = true;
            const body = { title: this.title, content: this.content };
            if (this.image.name) {
                body.image = this.image;
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
                this.posting = false;
            }
        },
        setImage(e) {
            if (e.target.files.length) {
                const imageFile = e.target.files[0];
                if (/^image\/*/.test(imageFile.type)) {
                    const reader = new FileReader();
                    reader.onload = () => {
                        this.image.name = imageFile.name;
                        this.image.content = reader.result;
                    };
                    reader.readAsDataURL(imageFile);
                    return;
                }
            }
            delete this.image.name;
            delete this.image.content;
        }
    }
});