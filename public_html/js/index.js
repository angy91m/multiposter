const app = new Vue({
    el: '#app',
    data: {
        content: '',
        imageName: '',
        imageContent: '',
        posting: false,
        showEmojiPicker: false,
        lastEmojiInputField: '',
    },
    methods: {
        async postContent() {
            this.posting = true;
            const body = { content: this.content };
            if (this.imageName) {
                body.image = {
                    name: this.imageName,
                    content: this.imageContent
                };
            }
            try {
                const res = await fetch('/post', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(body)
                });
                if (res.ok) {
                    this.content = '';
                    this.imageName = '';
                    this.imageContent = '';
                    const imgInput = document.getElementById('image');
                    imgInput.value = null;
                    imgInput.dispatchEvent(new Event('change'));
                    alert('Postato!');
                } else if (res.status === 400) {
                    try {
                        const {error} = await res.json();
                        alert('Errore: ' + error);
                    } catch {
                        alert('Qualcosa è andato storto');
                    }
                } else {
                    alert('Qualcosa è andato storto');
                }
            } catch {
                alert('Qualcosa è andato storto');
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
                        this.imageName = imageFile.name;
                        this.imageContent = reader.result;
                    };
                    reader.readAsDataURL(imageFile);
                    return;
                }
            }
            if (e.target.files.length) {
                alert('File non supportato');
                e.target.value = null;
                this.$nextTick(() => e.target.dispatchEvent(new Event('change')));
            }
            this.imageName = '';
            this.imageContent = '';
        },
        deleteImage() {
            this.imageName = '';
            this.imageContent = '';
            const imgInput = document.getElementById('image');
            imgInput.value = null;
            imgInput.dispatchEvent(new Event('change'));
        },
        setEmojiInputField(ref) {
            this.lastEmojiInputField = ref;
        },
        addEmojiToInput({detail: emoji}) {
            if (this.lastEmojiInputField) {
                const input = this.$refs[this.lastEmojiInputField],
                cursorPosition = input.selectionEnd,
                vKey = this.lastEmojiInputField.slice(0, -5),
                start = this[vKey].substring(0, input.selectionStart),
                end = this[vKey].substring(input.selectionStart);
                this[vKey] = `${start}${emoji.unicode}${end}`;
                input.focus();
                this.$nextTick(() => input.selectionEnd = cursorPosition + emoji.unicode.length);
            }
        },
        toggleEmojiPicker() {
            this.showEmojiPicker = !this.showEmojiPicker;
        }
    },
    mounted() {
        this.$refs.emojiPicker.addEventListener('emoji-click', this.addEmojiToInput);
    },
    beforeUnmount() {
        this.$refs.emojiPicker.removeEventListener('emoji-click', this.addEmojiToInput);
    }
});