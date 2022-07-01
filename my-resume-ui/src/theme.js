import { red } from '@material-ui/core/colors';
import { createTheme } from '@material-ui/core/styles';
// A custom theme for this app
const resumeTheme = theme => createTheme(theme, {
    palette: {
        type: 'light',
        error: {
            main: red.A400,
        },
        background: {
            // default: '#282c34',
        },
        success: {
            light: '#40b281'
          }
    },
    overrides: {
        MuiPaper: {
            root: {
                padding: '20px 10px',
                margin: '10px',
                // backgroundColor: '#fff', // 5d737e
            },
        },
        MuiButton: {
            root: {
                margin: '5px',
            },
        },
    },
});
export default resumeTheme;