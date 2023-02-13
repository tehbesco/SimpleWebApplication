/* The chat const defines the conversation.
 * 
 * It should be an object with numerical property names, and each property is an entry
 * in the conversation.
 * 
 * A conversation entry should have:
 *  - A "text" property that is what the chatbot says at this point in the conversation
 *  - Either:
 *     - A "next" property, which defines the next chat entry by stating a numerical key
 *       of the chat object and is used when the chatbot needs to say several things
 *       without input from the user
 *    OR
 *     - An "options" property that defines the choices a user can take this is an
 *       array of option objects
 * 
 * An options object should have:
 *  - a "text" property that is the label for the user's choice
 *  AND EITHER
 *  - a "next" property that defines the next chat entry by stating a numerical key of
 *    the chat object and is used when the user selects this option
 *  OR
 *  - a "url" property that defines a link for the user to be taken to
 * 
 * A simple example chat object is:
 * const chat = {
 *     1: {
 *         text: 'Good morning sir',
 *         next: 2
 *     },
 *     2: {
 *         text: 'Would you like tea or coffee with your breakfast?',
 *         options: [
 *             {
 *                 text: 'Tea',
 *                 next: 3
 *             },
 *             {
 *                 text: 'Coffee',
 *                 next: 4
 *             }
 *         ]
 *     },
 *     3: {
 *         text: 'Splendid - a fine drink if I do say so myself.'
 *     },
 *     4: {
 *         text: 'As you wish, sir'
 *     }
 * }
 */
const chat = {
    1: {
        text: 'Hi! I\'m Rabbit. BunnyHop\'s awesome chatbot. Can I help you with any issues you need resolved?',
        options: [
            {
                text: 'How do I order?',
                next: 2
            },
            {
                text: 'I have a question.',
                next: 3
            },
            {
                text: 'Issue with my order.',
                next: 4
            }
        ]
    },
    2: {
        text: 'You can order from our restaurants tab from the navbar! We deliver from a multitude of partnered restaurants!',
        options: [
            {
                text: 'Take me there!',
                url: "/foodSearch"
            }
        ]
    },
    3: {
        text: 'We have an FAQ page for commonly asked questions, if you have further issues you can write us a feedback form!',
        options: [
            {
                text: "Take me there!",
                url: "/faq"
            }
        ]
    },
    4: {
        text: 'Oh. Too bad. 🤪',
        options: [
            {
                text: "Oi.",
                next: 5
            }
            ]
    },
    5: {
        text: 'Kidding only la.',
        next: 6
    },
    6: {
        text: 'Visit this link.',
        options: [
            {
                text: "Click me",
                url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
            }
        ]
    }
};
