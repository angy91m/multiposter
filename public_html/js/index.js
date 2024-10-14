const app = new Vue({
    el: '#app',
    data: {
        content: '',
        image: {},
        posting: false,
        showEmojiPicker: false,
        lastEmojiInputField: ''
    },
    methods: {
        async postContent() {
            this.posting = true;
            const body = { content: this.content };
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