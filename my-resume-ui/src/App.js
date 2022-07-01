import './App.css';
import './index.css';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/grid';
import Item from '@material-ui/core/grid';
import Typography from '@material-ui/core/Typography';
import resumeTheme from './theme';
import { useTheme, createStyles, makeStyles, ThemeProvider } from '@material-ui/core/styles';
import DownloadPDF from './components/download-pdf';
import Resume from './components/resume';

const useStyles = makeStyles((theme) =>
  createStyles({
    mainTitle: {
      backgroundColor: theme.palette.primary.main,
      margin: '10px 0 30px 0',
      padding: '10px 0 10px 0',
      borderRadius: '10px',
      textTransform: 'uppercase',
      fontSize: '50px'
    },
    copyright: {
      color: theme.palette.info.main,
      margin: '10px 0 30px 0'
    }
  }),
);

function App() {
  const classes = useStyles(resumeTheme(useTheme()));

  return (
    <Container maxWidth="lg" className="App">
      <Typography variant="h1" component="h1" className={classes.mainTitle}>
        Professional Resume
      </Typography>
      <Resume />
      <Grid container spacing={3}>
        <Grid item lg={12} md={12}>
          <Item>
            <DownloadPDF />
          </Item>
        </Grid>
        <Grid item lg={12} container justifyContent='flex-end'>
          <Item>
            <Typography variant='body1' className={classes.copyright}>Copyright © 2022 Adrian Dolha.</Typography>
          </Item>
        </Grid>
      </Grid>

    </Container>
  );
}

export default App;
