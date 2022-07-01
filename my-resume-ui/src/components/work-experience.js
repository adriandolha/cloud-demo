import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Item from '@material-ui/core/Grid';
import { List, ListItem, ListItemIcon, ListItemText } from '@material-ui/core';
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';
import CircleIcon from '@mui/icons-material/Circle';
const useStyles = makeStyles((theme) =>
    createStyles({
        jobTitle: {
            float: 'left'
        },
        company: {
            float: 'left'
        },
        workExperience: {
            textTransform: 'uppercase',
            float: 'left'
        },
        work: {
            marginTop: '10px'
        },
        workDate: {
            fontStyle: 'italic',
            float: 'left',
            color: theme.palette.success.main,
        },
        tasks: {
            fontStyle: 'italic',
            float: 'left',
            color: theme.palette.success.main,
        },
        taskList: {
            listStyleType: 'circle'
        },
        taskListItem: {
            padding: '0 0 0 0',
            margin: '0 0 0 0'
        },
        techStack: {
            borderRadius: '10px',
            backgroundColor: theme.palette.primary.main,
            float: 'left',
            padding: '1px 10px 1px 10px',
            margin: '3px 3px 3px 3px',
            color: 'white'
        }
    }),
);

function WorkExperience({ data }) {
    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);
    console.log(data)
    return (
        <Grid item xs={12} md={8} lg={8} container direction='column'>
            <Item>
                <Typography variant="h5" className={classes.jobTitle}>
                    {data.jobTitle}
                </Typography>
            </Item>
            <Item>
                <Typography variant="h4" className={classes.company}>
                    {data.company}

                </Typography>
            </Item>
            <Item>
                <Typography variant="body1" align='left' className={classes.workDate}>
                    {data.from} - {data.to}
                </Typography>
            </Item>
            <Item>
                <Typography variant="body1" align='left' className={classes.tasks}>
                    Achievements/Tasks
                </Typography>
            </Item>
            <Item>

                <List className={classes.taskList} dense={true} disablePadding={true}>
                    {data.tasks && data.tasks.map(task => (
                        <ListItem className={classes.taskListItem} disableGutters={true} disablePadding={true}>
                            <CircleIcon sx={{ padding: '0 10px 0 0', margin: '0', fontSize: '8px', color: theme.palette.success.dark }} />
                            <Typography variant='body1'>{task}</Typography>
                        </ListItem>
                    ))}
                </List>
                {data.techStack && data.techStack.map(techStack => (
                    <Typography variant='body1' className={classes.techStack}>{techStack}</Typography>
                ))}

            </Item>
        </Grid>


    );
}

export default WorkExperience;
