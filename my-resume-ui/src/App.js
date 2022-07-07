import './App.css';
import './index.css';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/grid';
import Typography from '@material-ui/core/Typography';
import resumeTheme from './theme';
import { useTheme, createStyles, makeStyles, ThemeProvider } from '@material-ui/core/styles';
import DownloadPDF from './components/download-pdf';
import Resume from './components/resume';
import React, { useRef } from 'react';

const useStyles = makeStyles((theme) =>
  createStyles({
    mainTitle: {
      backgroundColor: theme.palette.primary.main,
      margin: '10px 0 30px 0',
      padding: '10px 0 10px 0',
      borderRadius: '10px',
      textTransform: 'uppercase',
      fontSize: '50px',
      color: 'white'
    },
    copyright: {
      color: theme.palette.info.main,
      margin: '10px 0 30px 0'
    }
  }),
);

function App() {
  const classes = useStyles(resumeTheme(useTheme()));
  const componentRef = useRef(null);

  return (
    <Container className="App" disableGutters={true}>
      <Typography variant="h1" component="h1" className={classes.mainTitle}>
        Professional Resume - Adrian Dolha
      </Typography>
      <Resume ref={componentRef} />

      <Grid container spacing={3}>
        <DownloadPDF resumeRef={componentRef} />
        <Grid item lg={12} container justifyContent='flex-end'>
          <Typography variant='body1' className={classes.copyright}>Copyright © 2022 Adrian Dolha.</Typography>
        </Grid>
      </Grid>

    </Container>
  );
}

export default App;
